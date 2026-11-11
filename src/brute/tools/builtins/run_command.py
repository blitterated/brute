import os
import subprocess

from .builtin_tool import BuiltinTool
from ..callable_tool import CallableTool
from ..tool_exception import ToolCommandException


class RunCommandTool(BuiltinTool):
    @property
    def routing_name(self) -> str:
        return "run_command"


    @property
    def schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.routing_name,
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


    async def run(self, args: dict) -> str:
        return str(self.run_command(**args))


    @CallableTool.tool_exception_handler
    def run_command(self, command):
        answer = input(f"Run '{command}'? [y/N] ")

        if answer.strip().lower() != "y":
            return "The user declined to run this command."

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=121
        )

        return_code = result.returncode
        output = (result.stdout + result.stderr).strip() or f"(no output, exit code {result.returncode})"

        if return_code > 0:
            raise ToolCommandException(f"run_command() returned a non-zero exit code: {return_code}\n\n{output}")

        return output
