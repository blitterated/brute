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

@pytest.mark.asyncio
async def test_mcp_stack(mcpTestConfigFile, std_err_logger):
    async with AsyncExitStack() as stack:
        # Arrange
        routing_name = "reverse"
        test_string = "Pack my box with five dozen liquor jugs!"
        tool_arguments = { "aString": test_string }
        expected_mcp_tool_response = "\n!sguj rouqil nezod evif htiw xob ym kcaP"

        mcp_mgr = McpServerManager(stack, mcpTestConfigFile(routing_name), std_err_logger)
        await mcp_mgr.launch_servers()

        tool_mgr = ToolManager(std_err_logger)
        tool_mgr.load_tools(mcp_mgr)

        # Act
        found_mcp_tool_response = await tool_mgr.call(routing_name, tool_arguments)

        # Assert
        assert found_mcp_tool_response == expected_mcp_tool_response


@pytest.mark.asyncio
async def test_tools_property(mcpTestConfigFile, std_err_logger):
    async with AsyncExitStack() as stack:
        # Arrange
        expected_mcp_tools = sorted([f"reverse_{x+1}" for x in range(5)])

        std_err_logger.debug(f"\ntest_tools_property: expected_mcp_tools:\n\t{expected_mcp_tools}") # DEBUG

        mcp_mgr = McpServerManager(stack, mcpTestConfigFile(*expected_mcp_tools), std_err_logger)
        await mcp_mgr.launch_servers()

        # Act
        found_mcp_tools = sorted([mcp.routing_name for mcp in mcp_mgr.tools])

        # Assert
        assert found_mcp_tools == expected_mcp_tools
