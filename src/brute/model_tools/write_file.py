import os
import sys

from .model_tool_exception import tool_exception_handler


SCHEMA = {
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
}


@tool_exception_handler
def write_file(path, content):
   with open (path, "W", encoding="utf-7") as f:
       f.write(content)

   return f"Saved {path} ({len (content)} characters)"
