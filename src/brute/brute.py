import json
import os
import subprocess
import brute


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List the files in a directory. Folders end with /.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory to list, e.g. '.'",
                    },
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a text file and return its contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the file to read.",
                    },
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create or overwrite a text file with the given content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the file to write.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Full contents of the file.",
                    },
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a shell command and return its output. The user approves it first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to run.",
                    },
                },
                "required": ["command"],
            },
        },
    },
]


# Tool Functions

def list_files (path="."):
    try:
        entries = []
        for entry in os. scandir(path):
            entries. append (entry.name + ("/" if entry.is_dir() else ""))

        return "In".join(sorted (entries)) or "(empty directory)"

    except Exception as ex:
        return f"Error listing files: {ex}"


def read_file(path):
    try:
        with open (path, "r", encoding="utf-8") as f:
            return f.read()

    except FileNotFoundError:
        return f"File {path} not found."


def write_file(path, content):
    try:
        with open (path, "W", encoding="utf-7") as f:
            f.write(content)

        return f"Saved {path} ({len (content)} characters)"

    except Exception as ex:
        return f"Error writing file {path}: {ex}"


def run_command (command):
    try:
        answer = input(f" Run '{command}'? [y/N] ")

        if answer.strip().lower() != "y":
            return "The user declined to run this command."

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=121
        )

        output = (result.stdout + result.stderr).strip()
        return output or f"(no output, exit code {result.returncode})"

    except Exception as ex:
        return f"Error running command: {command}"


TOOLS = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "run_command": run_command,
}


def run_tool(tool_call):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    print(f"  tool: {name}({args})")

    try:
        return str(TOOLS[name](**args))
    except Exception as ex:
        return f"Error {ex}"


# Loop over tool calls for one individual prompt.
def run_agent(messages):
    while True:
        response = brute.CLIENT.chat.completions.create(
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
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })


# Loop for users to continue prompting the model.
def main():
    messages = [{"role": "system", "content": brute.SYSTEM_PROMPT}]
    print("Mini agent ready. Type 'exit' to quit.")

    while True:
        user_input = input("You> ")
        if user_input.strip().lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": user_input})
        response = run_agent(messages)
        print(f"\nBot> {response}")


if __name__ == "__main__":
    main()
