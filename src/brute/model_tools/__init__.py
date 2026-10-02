import json
import model_tools.list_files
import model_tools.read_file
import model_tools.write_file
import model_tools.run_command


SCHEMAS = [
    model_tools.list_files.TOOL_SCHEMA,
    model_tools.read_file.TOOL_SCHEMA,
    model_tools.write_file.TOOL_SCHEMA,
    model_tools.run_command.TOOL_SCHEMA,
]


TOOLS = {
    "list_files": model_tools.list_files.list_files,
    "read_file": model_tools.read_file.read_file,
    "write_file": model_tools.write_file.write_file,
    "run_command": model_tools.run_command.run_command,
}


def run(tool_call):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    print(f"  tool: {name}({args}\n")

    try:
        return str(TOOLS[name](**args))
    except Exception as ex:
        return f"Error {ex}"
