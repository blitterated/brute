from . import list_files
from . import read_file
from . import write_file
from . import run_command


SCHEMAS = [
    list_files.TOOL_SCHEMA,
    read_file.TOOL_SCHEMA,
    write_file.TOOL_SCHEMA,
    run_command.TOOL_SCHEMA,
]


_TOOLS = {
    "list_files":  list_files.list_files,
    "read_file":   read_file.read_file,
    "write_file":  write_file.write_file,
    "run_command": run_command.run_command,
}


def run(name: str, args: dict) -> str:
    return str(_TOOLS[name](**args))
