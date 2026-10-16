from .list_files import list_files
from .read_file import read_file
from .write_file import write_file
from .run_command import run_command

from .list_files  import TOOL_SCHEMA as lf_schema
from .read_file   import TOOL_SCHEMA as rf_schema
from .write_file  import TOOL_SCHEMA as wf_schema
from .run_command import TOOL_SCHEMA as rc_schema

from .tool_exception_handler import tool_exception_handler
from .tool_exception_handler import ModelToolException


SCHEMAS = [
    lf_schema,
    rf_schema,
    wf_schema,
    rc_schema,
]


_TOOLS = {
    "list_files":  list_files,
    "read_file":   read_file,
    "write_file":  write_file,
    "run_command": run_command,
}


def run(name: str, args: dict) -> str:
    return str(_TOOLS[name](**args))
