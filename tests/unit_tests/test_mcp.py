import asyncio
import json
import pytest
import re

from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
#from mcp.client.stdio import stdio_client
from pathlib import Path

import brute.model_tools as mtools

from brute.brute import connect_mcp
from brute.brute import call_tool


@pytest.fixture()
def mcpTestConfigFile(tmp_path: Path) -> Path:
    """
    Generate and return an mcpServers.json file for testing purposes.

    This file is used by brute to identify and run MCP servers.
    In this case, it is just a simple string reversing MCP server.
    """
    mcpTestConfigContent = {
        "mcpServers": {
            "reverse": {
                "command": "uv",
                "args": [ "run", "tests/unit_tests/stdio_mcp_test_server.py" ]
            },
        }
    }
    mcpTestConfigFile = tmp_path / "mcpServers.json"
    mcpTestConfigFile.write_text(json.dumps(mcpTestConfigContent), encoding="utf-8")

    return mcpTestConfigFile


def test_show_mcpTestConfigFile(mcpTestConfigFile):
    print(f"\ntest_show_mcpTestConfigFile(): path:    {str(mcpTestConfigFile)}")
    with open(mcpTestConfigFile, 'r') as cfgFile:
        print(f"test_show_mcpTestConfigFile(): content: {cfgFile.read()}")


# Request:
#    {
#        "jsonrpc": "2.0",
#        "id": 42,
#        "method": "tools/call",
#        "params": {
#            "name": "reverse",
#            "arguments": {"aString": "Pack my box with five-dozen liquor jugs!"},
#        },
#    }

# Response:
#    {
#        "jsonrpc": "2.0",
#        "id": 42,
#        "result": {
#            "content": [{
#                "type":"text",
#                "text":"",
#            }],
#            "isError":false,
#        },
#    }

@pytest.mark.asyncio
async def test_mcp(mcpTestConfigFile):
    async with AsyncExitStack() as stack:
        # Arrange
        test_string = "Pack my box with five-dozen liquor jugs!"
        tool_request_id = 42
        tool_name = "reverse"
        tool_arguments = { "aString": test_string }

        print("test_mcp(): calling connect_mcp()") # DEBUG
        await connect_mcp(stack, mcpTestConfigFile)

        # Act
        print("test_mcp(): calling call_tool()") # DEBUG
        print(f"test_mcp(): {tool_name = }") # DEBUG
        print(f"test_mcp(): arguments:\n{json.dumps(tool_arguments)}") # DEBUG
        found_mcp_tool_response = await call_tool(tool_name, tool_arguments)

        print(f"test_mcp(): {found_mcp_tool_response =}") # DEBUG
