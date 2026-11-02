import json
import sys


RESPONSE_TO_INITIALIZE_CALL = {
    "protocolVersion": "2024-11-05",
    "capabilities": {
        "experimental": {},
        "prompts": {
            "listChanged": False,
        },
        "resources": {
            "subscribe": False,
            "listChanged": False,
        },
        "tools": {
            "listChanged": False,
        },
    },
    "serverInfo": {
        "name": "math",
        "version": "0.0.1",
    },
}


REVERSE_TOOL_SCHEMA = {
    "name": "reverse",
    "description": "Reverse a string.\n\nArgs:\n    a_string\n",
    "inputSchema": {
        "properties": {
            "a_string": {
                "title": "a_string",
                "type": "string",
            },
        },
        "required": ["a_string"],
        "type": "string",
    },
}


def emit(payload: dict) -> None:
    """Print one JSON object per line and flush immediately."""
    sys.stdout.write(json.dumps(payload, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def emit_result(request_id: int, result: object) -> None:
    if not isinstance(result, str) and not isinstance(result, dict):
        raise ValueError(f"result must be of type str or dict. {type(result)} was received.")

    emit({
       "jsonrpc": "2.0",
       "id": request_id,
       "result": result,
    })


def emit_mcp_error(message: str, code: int):
    emit(
        {
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": code,
                "message": message,
            },
        }
    )


def main() -> None:
    for raw_line in sys.stdin:
        line = raw_line.strip()

        if not line:
            continue

        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            emit_mcp_error(message="Parse error", code=-32700)
            continue

        if not isinstance(request, dict):
            emit_mcp_error(message="Invalid Request", code=-32600)
            continue

        method = request.get("method")
        request_id = request.get("id")

        if method == "initialize":
            #emit_result(request_id, RESPONSE_TO_INITIALIZE_CALL)
            emit(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": RESPONSE_TO_INITIALIZE_CALL,
                }
            )

        elif method == "notifications/initialized":
            # Do nothing, matching the bash script.
            continue

        elif method == "tools/list":
            emit(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": [
                            REVERSE_TOOL_SCHEMA,
                        ],
                    },
                }
            )

        elif method == "resources/list":
            emit(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "resources": [],
                    },
                }
            )

        elif method == "prompts/list":
            emit(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "prompts": [],
                    },
                }
            )

        elif method == "tools/call":
            params = request.get("params", {})
            if not isinstance(params, dict):
                params = {}

            _tool_name = params.get("name")

            arguments = params.get("arguments", {})
            if not isinstance(arguments, dict):
                arguments = {}

            a_string = arguments.get("num1")

            if a_string is "" or a_string is None:
                emit(
                    {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Missing or invalid argument: a_string must not be None or empty.",
                                }
                            ],
                            "isError": True,
                        },
                    }
                )
                continue

            reversed_string = a_string[::-1]

            emit(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"\n sum of two numbers is {reversed_string}",
                            }
                        ],
                        "isError": False,
                    },
                }
            )

        else:
            emit_mcp_error(message="Method not found", code=-32601)


if __name__ == "__main__":
    main()
