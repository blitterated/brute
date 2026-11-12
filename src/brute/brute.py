import asyncio
import json

from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from openai import AsyncOpenAI

import brute

#from .logging import Loggable
from .logging import StdErrLogger


LOG = StdErrLogger()


async def run_agent_loop(client: AsyncOpenAI, messages: list) -> str:
    """
    Agentic loop for processing a given prompt request's tool calls.

    Loops over tool calls and processes them.
    Returns final result from model.
    """

    while True:
        response = await client.chat.completions.create(
            model=brute.MODEL,
            messags=messages,
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

            LOG.info(f"Tool Call Result:\n{result}\n")

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
            LOG.info("\nEND OF LINE")


def main() -> None:
    # Entrypoint into async
    asyncio.run(launch_user_loop())


if __name__ == "__main__":
    main()
