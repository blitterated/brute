import builtins
import pytest
import re
import sys

from brute.logging import Loggable
from brute.tools import CallableTool, ToolManager

import brute.tools.builtins as btools


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


@pytest.fixture
def logger_mock() -> LoggerMock:
    return LoggerMock()


@pytest.fixture
def tool_mock() -> ToolMock:
    return ToolMock()


def p_stderr(text: str) -> None:
    print(text, file=sys.stderr)


def dump_tools(tool_mgr: ToolManager):
    p_stderr(f"\ntool_mgr id: {id(tool_mgr)}")

    existing_tools = tool_mgr.list_tools()
    p_stderr(f"\ntool count: {len(existing_tools)}")

    for et in existing_tools:
        p_stderr(f"\n\t{et}")


@pytest.mark.asyncio
async def test_add_tool(logger_mock: LoggerMock, tool_mock: ToolMock):
    tool_mgr = ToolManager(logger_mock)
    tool_mgr.add_tool(tool_mock)

    found_result = await tool_mgr.call(tool_mock.routing_name, tool_mock.canned_args)

    assert found_result == tool_mock.canned_run_response


@pytest.mark.asyncio
async def test_add_tool_throws_exception_with_duplicate_key(logger_mock: LoggerMock, tool_mock: ToolMock):
    expected_msg = f"'{tool_mock.routing_name}' already exists in ToolManager's collection. Remove it first."
    tool_mgr = ToolManager(logger_mock)

    # We don't care about this one
    tool_mgr.add_tool(tool_mock)

    with pytest.raises(Exception, match=re.escape(expected_msg)):
        tool_mgr.add_tool(tool_mock)
