import os
import sys

from ..callable_tool import CallableTool
from .builtin_tool import BuiltinTool


class WriteFileTool(BuiltinTool):
    @property
    def routing_name(self) -> str:
        return "write_file"


    @property
    def schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.routing_name,
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
        }


    async def run(self, args: dict) -> str:
        return str(self.write_file(**args))


    @CallableTool.tool_exception_handler
    def write_file(self, path, content):
        with open (path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Saved {path} ({len (content)} characters)"
