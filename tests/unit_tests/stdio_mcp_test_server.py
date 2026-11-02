import json
import sys

_ENABLE_LOGGING = True
#_ENABLE_LOGGING = False


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
    "description": "Reverse a string.\n\nArgs:\n    aString\n",
    "inputSchema": {
        "type": "object",
        "properties": {
            "aString": {
                "title": "aString",
                "type": "string",
                "description": "The target string to reverse.",
            },
        },
        "required": ["aString"],
    },
}


def log(msg: str) -> None:
    if _ENABLE_LOGGING:
        sys.stderr.write(f"[mcp-server] {msg}\n")
        sys.stderr.flush()


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

        log(f"STDIO_TEST_MCP: STDIO line in:\n{json.dumps(line, indent=2)}") # DEBUG

        if not line:
            continue

        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            emit_mcp_error(message="Parse error", code=-32700)
            continue

#        log("STDIO_TEST_MCP: Converted to JSON") # DEBUG

        if not isinstance(request, dict):
            emit_mcp_error(message="Invalid Request", code=-32600)
            continue

#        log("STDIO_TEST_MCP: Validated dict type") # DEBUG

        method = request.get("method")
#        log(f"STDIO_TEST_MCP: {method =}") # DEBUG
        request_id = request.get("id")
#        log(f"STDIO_TEST_MCP: {request_id =}") # DEBUG

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
            toolsListResponse = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        REVERSE_TOOL_SCHEMA,
                    ],
                },
            }

#            log(f"STDIO_TEST_MCP: toolsListResponse:\n{json.dumps(toolsListResponse, indent=2)}") # DEBUG

            # pydantic_core._pydantic_core.ValidationError: 1 validation error for ListToolsResult
            # tools.0.inputSchema.type
            #   Input should be 'object' [type=literal_error, input_value='string', input_type=str]
            #     For further information visit https://errors.pydantic.dev/2.13/v/literal_error
            emit(toolsListResponse)

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
            log(f"STDIO_TEST_MCP: params:\n{json.dumps(params, indent=2)}") # DEBUG

            tool_name = params.get("name") # Is this even used?
            log(f"STDIO_TEST_MCP: tool_name:\n{tool_name}") # DEBUG

            arguments = params.get("arguments", {})
            if not isinstance(arguments, dict):
                arguments = {}
            log(f"STDIO_TEST_MCP: arguments:\n{json.dumps(arguments, indent=2)}") # DEBUG

            aString = arguments.get("aString")
            log(f"STDIO_TEST_MCP: {aString =}") # DEBUG

            if aString == "" or aString is None:
                emit(
                    {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Missing or invalid argument: aString must not be None or empty.",
                                }
                            ],
                            "isError": True,
                        },
                    }
                )
                continue

            reversedString = aString[::-1]
            log(f"STDIO_TEST_MCP: {reversedString =}") # DEBUG

            emit(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"\n{reversedString}",
                            }
                        ],
                        "isError": False,
                    },
                }
            )

        else:
            emit_mcp_error(message="Method not found", code=-32601)

        log("STDIO_TEST_MCP: Exiting main()") # DEBUG


if __name__ == "__main__":
    main()
