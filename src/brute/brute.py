import json

from openai import AsyncOpenAI

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
_tool_schemas = brute.tools.schemas.copy()
_mcp_sessions: dict[str, ClientSession] = {}


async def connect_mcp(stack: AsyncExitStack, mcpConfigPath: Path) -> None:
    """Read in mcpServers.json config, merge in its tool schemas, and launch each MCP server."""
    config = json.loads(mcpConfigPath.read_text(encoding="utf-8"))

    if len(config["mcpServers"]) < 1:
        print("WARNING: mcpServers.json is empty.")

    for name, spec in config["mcpServers"].items():
        params = StdioServerParameters(command=spec["command"], args=spec["args"])

        try:
            read, write = await stack.enter_async_context(stdio_client(params))
            session = await stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
        except Exception as ex:
            print(f"ERROR: connect_mcp() failed to start '{name}'\n{ex}")
            continue

        tools = []
        try:
            tools = (await session.list_tools()).tools
        except Exception as ex:
            print(f"ERROR: session.list_tools() failed: '{name}'\n{ex}")
            continue

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
        print(f"MCP connected '{name}': {[t.name for t in tools]}")


async def call_tool(tool_name: str, tool_args: dict) -> str:
    """Map a tool call by name to a function or mcp client and call it."""
    print(f"Tool Call Request:\n\t{tool_name}({tool_args}")

    # Try local tools first.
    if brute.tools.is_local(tool_name):
        return brute.tools.run(tool_name, tool_args)

    # Otherwise, run an MCP request.
    try:
        result = await _mcp_sessions[tool_name].call_tool(tool_name, tool_args)
        return "\n".join(c.text for c in result.content if hasattr(c, "text"))
    except Exception as ex:
        return f"Error running tool call:\n{type(ex).__name__}: {ex}"


async def run_agent_loop(client: AsyncOpenAI, messages: list) -> str:
    """
    Agentic loop for processing a given prompt request's tool calls.

    Loops over tool calls and processes them.
    Returns final result from model.
    """

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

        # tool_call: openai.types.chat.chat_completion_message_function_tool_call.ChatCompletionMessageFunctionToolCall
        for tool_call in response_msg.tool_calls:

            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            result = await call_tool(tool_name, tool_args)

            print(f"Tool Call Result:\n{result}\n")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })


async def run_user_loop(client: AsyncOpenAI, messages: list) -> None:
    """
    Continuous loop for handling successive user inputs.

    Captures prompting from user.
    Appends prompt to message history.
    Sends above into agent loop.
    Shows the result.
    """
    while True:
        user_input = await asyncio.to_thread(input, "\nYou: ")

        if user_input.strip().lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": user_input})
        response = await run_agent_loop(client, messages)
        print(f"\nBot> {response}\n")


async def launch_user_loop() -> None:
    """
    Initialize and enter the user loop.

    Creates a client.
    Creates the messages array and initializes with system prompt.
    Enters the user prompt loop.
    """
    async with AsyncExitStack() as stack:
        await connect_mcp(stack, MCP_CONFIG)

        client = brute.client.create_async()
        messages = [{"role": "system", "content": brute.SYSTEM_PROMPT}]

        print("I am brute! Quit with 'exit', 'quit', or Ctrl-c.\n")

        try:
            await run_user_loop(client, messages)
        except(EOFError, KeyboardInterrupt):
            print("\nEND OF LINE")


def main() -> None:
    # Entrypoint into async
    asyncio.run(launch_user_loop())


if __name__ == "__main__":
    main()
