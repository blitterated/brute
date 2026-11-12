import asyncio
import json
import pytest
import re

from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from pathlib import Path

from brute.logging import StdErrLogger
from brute.tools import ToolManager
from brute.tools.mcp import McpServerManager

TEST_TOOL_NAME = "reverse"


@pytest.fixture()
def mcpTestConfigFile(tmp_path: Path) -> Path:
    """
    Generate and return an mcpServers.json file for testing purposes.

    This file is used by brute to identify and run MCP servers.
    In this case, it is just a simple string reversing MCP server.
    """
    mcpTestConfigContent = {
        "mcpServers": {
            TEST_TOOL_NAME: {
                "command": "uv",
                "args": [ "run", "tests/unit_tests/stdio_mcp_test_server.py" ]
            },
        }
    }
    mcpTestConfigFile = tmp_path / "mcpServers.json"
    mcpTestConfigFile.write_text(json.dumps(mcpTestConfigContent), encoding="utf-8")

    return mcpTestConfigFile


def test_show_mcpTestConfigFile(mcpTestConfigFile: Path, std_err_logger: StdErrLogger):
    std_err_logger.debug(f"\ntest_show_mcpTestConfigFile(): path:    {str(mcpTestConfigFile)}")
    with open(mcpTestConfigFile, 'r') as cfgFile:
        std_err_logger.debug(f"test_show_mcpTestConfigFile(): content: {cfgFile.read()}")


@pytest.mark.asyncio
async def test_mcp(mcpTestConfigFile, std_err_logger):
    async with AsyncExitStack() as stack:
        # Arrange
        test_string = "Pack my box with five-dozen liquor jugs!"
        tool_request_id = 42
        tool_arguments = { "aString": test_string }
        expected_mcp_tool_response = "\n!sguj rouqil nezod-evif htiw xob ym kcaP"

        mcp_mgr = McpServerManager(stack, mcpTestConfigFile, std_err_logger)
        await mcp_mgr.launch_servers()

        tool_mgr = ToolManager(std_err_logger)
        tool_mgr.load_tools(mcp_mgr)

        # Act
        found_mcp_tool_response = await tool_mgr.call(TEST_TOOL_NAME, tool_arguments)

        # Assert
        assert found_mcp_tool_response == expected_mcp_tool_response





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

