import os

from . import tool_exception_handler as tex


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


@tex.tool_exception_handler
def list_files (path="."):

    print(f"list_files(): path = '{path}'") # DEBUG

    entries = []
    for entry in os.scandir(path):
        fmtd_entry = entry.name + ("/" if entry.is_dir() else "")
        entries.append(fmtd_entry)
        print(f"list_files entry: {fmtd_entry}") # DEBUG

    dir_list = '\n'.join(sorted(entries)) or "(empty directory)"
    print(f"list_files(): repr(dir_list)\n{repr(dir_list)}\n") # DEBUG
    print(f"list_files(): dir_list\n{dir_list}\n") # DEBUG

    return dir_list
