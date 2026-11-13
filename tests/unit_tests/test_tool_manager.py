import builtins
import pytest
import re
import sys

from collections.abc import Sequence

import brute.tools.builtins as btools

from brute.logging import Loggable
from brute.tools import CallableTool, ToolManager, LoadableTools


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
    run_args: list[dict] = []
    canned_run_response = "Your call is important to us. Please hold."
    run_param_name: str = "motion"
    run_param_value: str = "ocean"
    canned_args = { run_param_name: run_param_value }

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
                        self.run_param_name: {
                            "type": "string",
                            "description": "Is it in the ocean?",
                        },
                    },
                    "required": [self.run_param_name],
                },
            },
        }

    async def run(self, args: dict) -> str:
        self.run_args.append(args)
        return self.canned_run_response


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
    tool_mgr = ToolManager(logger_mock)
    tool_mgr.add_tool(tool_mock)

    found_result = await tool_mgr.call(tool_mock.routing_name, tool_mock.canned_args)

    assert found_result == tool_mock.canned_run_response


def test_add_tool_throws_exception_with_duplicate_key(logger_mock: LoggerMock, tool_mock: ToolMock):
    expected_msg = f"'{tool_mock.routing_name}' already exists in ToolManager's collection. Remove it first."
    tool_mgr = ToolManager(logger_mock)

    # Add the tool to the empty ToolManager.
    tool_mgr.add_tool(tool_mock)

    # Adding the tool again should throw an exception.
    with pytest.raises(Exception, match=re.escape(expected_msg)):
        tool_mgr.add_tool(tool_mock)


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
    p_stderr("\ntest_remove_tool_with_fully_populated_toolmanager\n") # DEBUG
    p_stderr("LoadableToolsStub tools:") # DEBUG
    for t in loadable_tools_stub.tools: # DEBUG
        p_stderr(f"\t{t.routing_name}") # DEBUG

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
    p_stderr("\ntest_remove_tool_with_mostly_populated_toolmanager\n") # DEBUG

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
    p_stderr("\n_test_remove_tool_with_populated_toolmanager\n") # DEBUG

    # Arrange
    tool_mgr = ToolManager(logger_mock)
    tool_mgr.load_tools(loadable_tools_stub)
    if should_add_tool_mock:
        tool_mgr.add_tool(tool_mock)

    expected_count:   int = len(loadable_tools_stub.tools)
    expected_result: bool = should_add_tool_mock

    p_stderr("ToolManager tools BEFORE") # DEBUG
    dump_tools(tool_mgr) # DEBUG

    # Act
    found_result = tool_mgr.remove_tool(tool_mock)

    p_stderr("ToolManager tools AFTER") # DEBUG
    dump_tools(tool_mgr) # DEBUG

    # Assert
    assert len(tool_mgr.list_tools()) == expected_count
    assert found_result == expected_result
    assert tool_mock.routing_name not in tool_mgr.list_tools()
