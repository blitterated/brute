import builtins
import pytest
import re
import sys

from collections.abc import Callable
from collections.abc import Sequence
from contextlib import AsyncExitStack
from pathlib import Path

import brute.tools.builtins as btools

from brute.logging import Loggable, StdErrLogger
from brute.tools import CallableTool, LoadableTools, ToolManager
from brute.tools.mcp import McpServerManager


############################################################
# Mocks and Stubs                                          #
############################################################

class LoggerMock(Loggable):
    def __init__(self):
        self.messages: list[tuple[str, str]] = []

    def debug(self, message: str) -> None:
        self.messages.append( ("debug", message) )

    def info(self, message: str) -> None:
        self.messages.append( ("info", message) )

    def warn(self, message: str) -> None:
        self.messages.append( ("warn", message) )

    def error(self, message: str) -> None:
        self.messages.append( ("error", message) )

    def log(self, message: str) -> None:
        self.messages.append( ("log", message) )


class ToolMock(CallableTool):
    def __init__(self):
        self.found_args: list[dict] = []
        self.param_name: str = "airhose"
        self.canned_response: str = "His airhose broke"

    @property
    def routing_name(self) -> str:
        return "mock_lobster"

    @property
    def schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.routing_name,
                "description": "Mock a callable tool and capture usage.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        self.param_name: {
                            "type": "string",
                            "description": "Returns a statement of airhose status.",
                        },
                    },
                    "required": [self.param_name],
                },
            },
        }

    async def run(self, args: dict) -> str:
        self.found_args.append(args)
        return self.canned_response


class LoadableToolsStub(LoadableTools):
    @property
    def tools(self) -> Sequence[CallableTool]:
        return [
            btools.ListFilesTool(),
            btools.ReadFileTool(),
            btools.WriteFileTool(),
            btools.RunCommandTool(),
        ]


############################################################
# Fixtures                                                 #
############################################################

@pytest.fixture
def logger_mock() -> LoggerMock:
    return LoggerMock()


@pytest.fixture
def tool_mock() -> ToolMock:
    return ToolMock()


@pytest.fixture
def loadable_tools_stub() -> LoadableToolsStub:
    return LoadableToolsStub()


############################################################
# Quick-n-Dirty STDERR Logging                             #
############################################################

def p_stderr(text: str) -> None:
    print(text, file=sys.stderr)


def dump_tools(tool_mgr: ToolManager):
    p_stderr(f"tool_mgr id: {id(tool_mgr)}")

    existing_tools = tool_mgr.list_tools()
    p_stderr(f"tool count: {len(existing_tools)}")

    for et in existing_tools:
        p_stderr(f"\t{et}")


############################################################
# Tests                                                    #
############################################################

@pytest.mark.asyncio
async def test_add_tool(logger_mock: LoggerMock, tool_mock: ToolMock):
    # Arrange
    tool_mgr = ToolManager(logger_mock)
    tool_mgr.add_tool(tool_mock)

    tool_mgr = ToolManager(logger_mock)
    tool_mgr.add_tool(tool_mock)

    tool_args = { tool_mock.param_name: "broke" }

    # Act
    found_result = await tool_mgr.call(tool_mock.routing_name, tool_args)

    # Assert
    assert found_result == tool_mock.canned_response


def test_add_tool_throws_exception_with_duplicate_key(logger_mock: LoggerMock, tool_mock: ToolMock):
    expected_msg = f"'{tool_mock.routing_name}' already exists in ToolManager's collection. Remove it first."
    tool_mgr = ToolManager(logger_mock)

    # Add the tool to the empty ToolManager.
    tool_mgr.add_tool(tool_mock)

    # Adding the tool again should throw an exception.
    with pytest.raises(Exception, match=re.escape(expected_msg)):
        tool_mgr.add_tool(tool_mock)


def test_load_tools(
        logger_mock: LoggerMock,
        loadable_tools_stub: LoadableToolsStub,
    ):
    # Arrange
    tool_mgr = ToolManager(logger_mock)

    # Act
    tool_mgr.load_tools(loadable_tools_stub)

    # Acquire
    expected_tools: list[str] = [t.routing_name for t in loadable_tools_stub.tools]
    found_tools: list[str] = tool_mgr.list_tools()

    # Assert
    assert len(found_tools) == len(expected_tools)
    for t in expected_tools:
        assert t in found_tools


def test_remove_tool_with_empty_toolmanager(logger_mock: LoggerMock, tool_mock: ToolMock):
    tool_mgr = ToolManager(logger_mock)
    expected_result = False

    found_result = tool_mgr.remove_tool(tool_mock)

    assert len(tool_mgr.list_tools()) == 0
    assert found_result == expected_result


def test_remove_tool_with_fully_populated_toolmanager(
        logger_mock: LoggerMock,
        loadable_tools_stub: LoadableToolsStub,
        tool_mock: ToolMock
    ):
    _test_remove_tool_with_populated_toolmanager(
        logger_mock,
        loadable_tools_stub,
        tool_mock,
        True
    )


def test_remove_tool_with_mostly_populated_toolmanager(
        logger_mock: LoggerMock,
        loadable_tools_stub: LoadableToolsStub,
        tool_mock: ToolMock
    ):
    _test_remove_tool_with_populated_toolmanager(
        logger_mock,
        loadable_tools_stub,
        tool_mock,
        False
    )


def _test_remove_tool_with_populated_toolmanager(
        logger_mock: LoggerMock,
        loadable_tools_stub: LoadableToolsStub,
        tool_mock: ToolMock,
        should_add_tool_mock: bool,
    ):
    # Arrange
    tool_mgr = ToolManager(logger_mock)
    tool_mgr.load_tools(loadable_tools_stub)
    if should_add_tool_mock:
        tool_mgr.add_tool(tool_mock)

    expected_count:   int = len(loadable_tools_stub.tools)
    expected_result: bool = should_add_tool_mock

    # Act
    found_result = tool_mgr.remove_tool(tool_mock)

    # Assert
    assert len(tool_mgr.list_tools()) == expected_count
    assert found_result == expected_result
    assert tool_mock.routing_name not in tool_mgr.list_tools()


@pytest.mark.asyncio
async def test_builtin_tools_property(
        logger_mock: LoggerMock,
        loadable_tools_stub: LoadableToolsStub,
        tool_mock: ToolMock,
        mcpTestConfigFile: Callable[[str], Path],
    ):
    async with AsyncExitStack() as stack:
        # Arrange
        test_tool_name = "reverse"

        mcp_mgr = McpServerManager(stack, mcpTestConfigFile(test_tool_name), logger_mock)
        await mcp_mgr.launch_servers()

        tool_mgr = ToolManager(logger_mock)
        tool_mgr.load_tools(loadable_tools_stub)
        tool_mgr.load_tools(mcp_mgr)
        tool_mgr.add_tool(tool_mock)

        expected_builtin_tools: list[str] = [t.routing_name for t in loadable_tools_stub.tools]

        # Act
        found_builtin_tools: dict[str, CallableTool] = tool_mgr.builtin_tools

        # Assert
        assert len(found_builtin_tools) == len(expected_builtin_tools)
        for xt in expected_builtin_tools:
            assert xt in found_builtin_tools


@pytest.mark.asyncio
async def test_mcp_tools_property(
        logger_mock: LoggerMock,
        loadable_tools_stub: LoadableToolsStub,
        tool_mock: ToolMock,
        mcpTestConfigFile: Callable[[str], Path],
    ):
    async with AsyncExitStack() as stack:
        # Arrange
        test_tool_name = "reverse"

        mcp_mgr = McpServerManager(stack, mcpTestConfigFile(test_tool_name), logger_mock)

        await mcp_mgr.launch_servers()

        tool_mgr = ToolManager(logger_mock)
        tool_mgr.load_tools(loadable_tools_stub)
        tool_mgr.load_tools(mcp_mgr)
        tool_mgr.add_tool(tool_mock)

        expected_mcp_tools: list[str] = [t.routing_name for t in mcp_mgr.tools]

        # Act
        found_mcp_tools: dict[str, CallableTool] = tool_mgr.mcp_tools

        # Assert
        assert len(found_mcp_tools) == len(expected_mcp_tools)
        for xt in expected_mcp_tools:
            assert xt in found_mcp_tools


@pytest.mark.asyncio
async def test_call(
        logger_mock: LoggerMock,
        tool_mock: ToolMock,
    ):
    async with AsyncExitStack() as stack:
        # Arrange
        tool_mgr = ToolManager(logger_mock)
        tool_mgr.add_tool(tool_mock)

        tool_args = { tool_mock.param_name: "broke" }

        # Act
        found_result = await tool_mgr.call(tool_mock.routing_name, tool_args)

        # Assert
        assert found_result == tool_mock.canned_response
        assert tool_mock.found_args == [tool_args]
