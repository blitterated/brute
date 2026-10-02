import brute.model_client.client as client
import brute.model_tools as tools
import brute


CLIENT = client.create()


# Loop over tool calls for one individual prompt.
def run_agent(messages):
    while True:
        response = CLIENT.chat.completions.create(
            model=brute.MODEL,
            messages=messages,
            tools=tools.SCHEMAS,
        )
        response_msg = response.choices[0].message
        messages.append(response_msg)

        # No tool calls means the model finished and gave us an answer.
        if not response_msg.tool_calls:
            return response_msg.content

        for tool_call in response_msg.tool_calls:
            result = tools.run(tool_call)
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
