from .list_files import list_files
from .read_file import read_file
from .write_file import write_file
from .run_command import run_command

from .list_files  import SCHEMA as lf_schema
from .read_file   import SCHEMA as rf_schema
from .write_file  import SCHEMA as wf_schema
from .run_command import SCHEMA as rc_schema

from .model_tool_exception import ModelToolException
from .model_tool_exception import tool_exception_handler


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
