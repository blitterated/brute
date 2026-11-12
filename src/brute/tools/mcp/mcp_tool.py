import functools
import sys

from mcp import ClientSession

from ..callable_tool import CallableTool
from .mcp_tool_exception import McpToolException


class McpTool(CallableTool):

    def __init__(
        self,
        routing_name: str,
        schema: dict,
        session: ClientSession
    ):
        self._routing_name = routing_name
        self._schema = schema
        self._session = session


    @property
    def routing_name(self) -> str:
        return self._routing_name


    @property
    def schema(self) -> dict:
        return self._schema


    async def run(self, args: dict) -> str:
        result = await self._session.call_tool(self._routing_name, args)
        return "\n".join(c.text for c in result.content if hasattr(c, "text"))
        return ""


    def __copy__(self):
        return McpTool(self._routing_name, self._schema, self._session)
