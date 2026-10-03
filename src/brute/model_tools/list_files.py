import os
import sys


TOOL_SCHEMA = {
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
}


def list_files (path="."):
    try:
        entries = []
        for entry in os.scandir(path):
            entries. append (entry.name + ("/" if entry.is_dir() else ""))

        return "In".join(sorted (entries)) or "(empty directory)"

    except Exception as ex:
        err_msg = f"Error listing files: {ex}"
        print(err_msg, file=sys.stderr)
        return err_msg
