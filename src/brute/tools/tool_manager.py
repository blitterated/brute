from contextlib import AsyncExitStack
from pathlib import Path

from .callable_tool import CallableTool
from .loadable_tools import LoadableTools
from ..logging import Loggable
from .builtins import BuiltinTool
from .mcp import McpTool


class ToolManager:
    _tools: dict[str, CallableTool] = {}


    def __init__(self, log: Loggable):
        self._log: Loggable = log


    def add_tool(self, tool: CallableTool) -> None:
        key = tool.routing_name

        if key in self._tools:
            raise Exception(f"'{key}' already exists in ToolManager's collection. Remove it first.")

        self._tools[key] = tool


    def load_tools(self, loadable: LoadableTools) -> None:
        for tool in loadable.tools:
            self.add_tool(tool)


    def remove_tool(self, tool: CallableTool) -> bool:
        key = tool.routing_name
        key_found = False

        if key in self._tools:
            del self._tools[key]
            key_found = True

        return key_found


    @property
    def builtin_tools(self) -> dict[str, CallableTool]:
        return {k: v for k, v in self._tools if isinstance(v, BuiltinTool)}


    @property
    def mcp_tools(self) -> dict[str, CallableTool]:
        return {k: v for k, v in self._tools if isinstance(v, McpTool)}


    async def call(self, name: str, args: dict) -> str:
        """Call a CallableTool in the ToolManager's collection."""
        self._log.info(f"Tool Call Request:\n\t{name}({args}")

        # Bail if tool doesn't exist
        if not name in self._tools:
            raise Exception(f"\"{name}\" tool is not in ToolManager's collection.")

        try:
            return await self._tools[name].run(args)
        except Exception as ex:
            return f"Error running tool call for '{name}':\n{type(ex).__name__}: {ex}"
