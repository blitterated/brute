import os

from ..callable_tool import CallableTool
from .builtin_tool import BuiltinTool


class ListFilesTool(BuiltinTool):
    @property
    def routing_name(self) -> str:
        return "list_files"


    @property
    def schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.routing_name,
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
        }


    async def run(self, args: dict) -> str:
        return str(self.list_files(**args))


    @CallableTool.tool_exception_handler
    def list_files(self, path="."):
        entries = []
        for entry in os.scandir(path):
            fmtd_entry = entry.name + ("/" if entry.is_dir() else "")
            entries.append(fmtd_entry)

        dir_list = '\n'.join(sorted(entries)) or "(empty directory)"
        return dir_list
