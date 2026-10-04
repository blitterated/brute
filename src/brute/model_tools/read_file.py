import os
import tool_exception_handler as tex


TOOL_SCHEMA = {
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
}


@tex.tool_exception_handler
def read_file(path):
    with open (path, "r", encoding="utf-8") as f:
        return f.read()
