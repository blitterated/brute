import json
import brute


_CLIENT = brute.client.create()


def run_tool(tool_call):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    print(f"  tool: {name}({args}\n")

    try:
        return brute.tools.run(tool_call, args)
    except Exception as ex:
        return f"Error {ex}"


# Loop over tool calls for one individual prompt.
def run_agent(messages):
    while True:
        response = _CLIENT.chat.completions.create(
            model=brute.MODEL,
            messages=messages,
            tools=brute.tools.SCHEMAS,
        )
        response_msg = response.choices[0].message
        messages.append(response_msg)

        # No tool calls means the model finished and gave us an answer.
        if not response_msg.tool_calls:
            return response_msg.content

        for tool_call in response_msg.tool_calls:
            result = run_tool(tool_call)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })


# Loop for users to continue prompting the model.
def main():
    messages = [{"role": "system", "content": brute.SYSTEM_PROMPT}]
    print("Mini agent ready. Type 'exit' to quit.\n")

    while True:
        user_input = input("You> ")
        print()
        if user_input.strip().lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": user_input})
        response = run_agent(messages)
        print(f"\nBot> {response}\n")


if __name__ == "__main__":
    main()
