import json

# Imports for MCP
import asyncio
from contextlib import AsyncExitStack
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import brute


# Project Paths config
PROJECT_ROOT = Path(__file__).parent
MCP_CONFIG = PROJECT_ROOT / "mcp_servers.json"


# Tool config
_tool_schemas = brute.tools.SCHEMAS.copy()
_mcp_sessions: dict[str, ClientSession] = {}


async def connect_mcp(stack: AsyncExitStack, mcpConfigPath: Path):
    """Read in mcpServers.json config, merge in its tool schemas, and launch each MCP server."""
    config = json.loads(MCP_CONFIG.read_text(encoding="utf-8"))

    for name, spec in config["mcpServers"].items():
        params = StdioServerParameters(command=spec["command"], args=spec["args"])

        try:
            read, write = await stack.enter_async_context(stdio_client(params))
            session = await stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
        except Exception as ex:
            print(f"ERROR: connect_mcp() failed to start '{name}'\n{ex}")
            continue

        tools = (await session.list_tools()).tools
        for tool in tools:
            _mcp_sessions[tool.name] = session
            _tool_schemas.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.input_schema,
                    },
            })
        print(f"MCP connected '{name}': {[t.name for t in tools]}") # DEBUG


async def call_tool(name: str, args: dict) -> str:
    """Run a tool, either ours directly, or an MCP server's over the protocol."""

    # Try local tools, our functions defined above, first.
    if brute.tools.is_local(name):
        return brute.tools.run(name, args)

    # Otherwise, run an MCP request.
    result = await _mcp_sessions[name].call_tool(name, args)
    return "\n".join(c.text for c in result.content if hasattr(c, "text"))


async def run_tool(tool_call):
    """Map a tool call by name to a function or mcp client."""
    tool_name = tool_call.function.name
    tool_args = json.loads(tool_call.function.arguments)
    print(f"Tool Call Request:\n{tool_name}({tool_args}\n") # DEBUG

    try:
        return await call_tool(tool_name, tool_args)
    except Exception as ex:
        return f"Error running tool call:\n{ex}"


async def run_agent(client, messages):
    """Agent loop for processing a given prompt request's tool calls."""

    while True:
        response = await client.chat.completions.create(
            model=brute.MODEL,
            messages=messages,
            tools=_tool_schemas,
        )
        response_msg = response.choices[0].message
        messages.append(response_msg)

        # No tool calls means the model finished and gave us an answer.
        if not response_msg.tool_calls:
            return response_msg.content

        for tool_call in response_msg.tool_calls:
            result = await run_tool(tool_call)
            print(f"Tool Call Result:\n{result}\n") # DEBUG
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })


async def run_user_loop(client, messages):
   """Continuous loop for handling successive user inputs."""
   while True:
       question = await asyncio.to_thread(input, "\nYou: ")
       messages.append({"role": "user", "content": question})
       response = await run_agent(client, messages)
       print(f"\nBot> {response}\n")


async def launch_user_loop():
    """User loop for continued prompting."""
    async with AsyncExitStack() as stack:
        await connect_mcp(stack, MCP_CONFIG)

        client = brute.client.create_async()
        messages = [{"role": "system", "content": brute.SYSTEM_PROMPT}]

        print("Mini agent ready. Type 'exit' to quit.\n")

        try:
            await run_user_loop(client, messages)
        except(EOFError, KeyboardInterrupt):
            print("\nEND OF LINE")


# Entrypoint into async
def main():
    asyncio.run(launch_user_loop())


if __name__ == "__main__":
    main()
