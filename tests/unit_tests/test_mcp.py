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
                "command": "uv run",
                "args": [ "stdio_mcp_test_server.py" ]
            },
        }
    }
    mcpTestConfigFile = tmp_path / "mcpServers.json"

    print(f"\nmcpTestConfigFile(): path:    {str(mcpTestConfigFile)}") # DEBUG

    mcpTestConfigFile.write_text(json.dumps(mcpTestConfigContent), encoding="utf-8")

    with open(str(mcpTestConfigFile), 'r') as fart: # DEBUG
        print(f"mcpTestConfigFile(): content: {fart.read()}") # DEBUG

    return mcpTestConfigFile


def test_show_mcpTestConfigFile(mcpTestConfigFile):
    print(f"test_show_mcpTestConfigFile(): path:    {str(mcpTestConfigFile)}") # DEBUG
    with open(mcpTestConfigFile, 'r') as cfgFile:
        print(f"test_show_mcpTestConfigFile(): content: {cfgFile.read()}") # DEBUG


# Request:
#    {
#        "jsonrpc": "2.0",
#        "id": 42,
#        "method": "tools/call",
#        "params": {
#            "name": "reverse",
#            "arguments": {"a_string": "Pack my box with five-dozen liquor jugs!"},
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
        tool_params = {
            "name": tool_name,
            "arguments": { "a_string": test_string },
        }

        print(f"test_mcp(): path:    {str(mcpTestConfigFile)}") # DEBUG
        with open(str(mcpTestConfigFile), 'r') as fart: # DEBUG
            print(f"test_mcp(): content: {fart.read()}") # DEBUG

        await connect_mcp(stack, mcpTestConfigFile)

        # Act
        found_mcp_tool_response = await call_tool(tool_name, tool_params)

        print(f"test_mcp(): {found_mcp_tool_response =}") # DEBUG
