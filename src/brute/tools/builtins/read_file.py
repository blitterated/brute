import os

from ..callable_tool import CallableTool
from .builtin_tool import BuiltinTool


class ReadFileTool(BuiltinTool):
    @property
    def routing_name(self) -> str:
        return "read_file"


    @property
    def schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.routing_name,
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
        }


    async def run(self, args: dict) -> str:
        return str(self.read_file(**args))


    @CallableTool.tool_exception_handler
    def read_file(self, path):
        with open (path, "r", encoding="utf-8") as f:
            return f.read()
