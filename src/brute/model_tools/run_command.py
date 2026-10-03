import os
import subprocess
import sys


TOOL_SCHEMA = {
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
}


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
        err_msg = f"Error running command: {command}"
        print(err_msg, file=sys.stderr)
        return err_msg
