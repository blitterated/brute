import os
import sys


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


def read_file(path):
    try:
        with open (path, "r", encoding="utf-8") as f:
            return f.read()

    except FileNotFoundError:
        err_msg = f"File {path} not found."
        print(err_msg, file=sys.stderr)
        return err_msg
