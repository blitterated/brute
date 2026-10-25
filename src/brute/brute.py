import json

# Imports for MCP
#import asyncio
#from contextlib import AsyncExitStack
#from pathlib import Path
#from mcp import ClientSession, StdioServerParameters
#from mcp.client.stdio import stdio_client

import brute


TOOL_SCHEMAS = brute.tools.SCHEMAS


def run_tool(tool_call):
    """Map a tool call by name to a function."""
    tool_name = tool_call.function.name
    tool_args = json.loads(tool_call.function.arguments)
    print(f"Tool Call Request:\n{tool_name}({tool_args}\n") # DEBUG

    try:
        return brute.tools.run(tool_name, tool_args)
    except Exception as ex:
        return f"Error running tool call:\n{ex}"


def run_agent(client, messages):
    """Agent loop for processing a given prompt request's tool calls."""

    while True:
        response = client.chat.completions.create(
            model=brute.MODEL,
            messages=messages,
            tools=TOOL_SCHEMAS,
        )
        response_msg = response.choices[0].message
        messages.append(response_msg)

        # No tool calls means the model finished and gave us an answer.
        if not response_msg.tool_calls:
            return response_msg.content

        for tool_call in response_msg.tool_calls:
            result = run_tool(tool_call)
            print(f"Tool Call Result:\n{result}\n") # DEBUG
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })


def main():
    """User loop for continued prompting."""

    client = brute.client.create()

    messages = [{"role": "system", "content": brute.SYSTEM_PROMPT}]
    print("Mini agent ready. Type 'exit' to quit.\n")

    while True:
        user_input = input("You> ")
        print()
        if user_input.strip().lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": user_input})
        response = run_agent(client, messages)
        print(f"\nBot> {response}\n")


if __name__ == "__main__":
    main()
