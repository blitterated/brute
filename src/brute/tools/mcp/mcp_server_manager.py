import asyncio
import json

from collections.abc import Sequence
from copy import copy
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pathlib import Path

import brute

from ..callable_tool import CallableTool
from ...logging import Loggable
from ..loadable_tools import LoadableTools
from .mcp_tool import McpTool


class McpServerManager(LoadableTools):
    # Project Paths config
    #_projectRoot = Path(__file__).parent
    #_mcpConfig = _projectRoot / "mcp_servers.json"


    def __init__(self, stack: AsyncExitStack, mcpConfigPath: Path, log: Loggable):
        self._stack: AsyncExitStack = stack
        self._log: Loggable = log

        mcpConfig: str = mcpConfigPath.read_text(encoding="utf-8") # DEBUG
        self._log.debug(f"McpServerManager.__init__: mcpConfig:\n{mcpConfig}") # DEBUG
        self._mcp_configs: dict = json.loads(mcpConfig)["mcpServers"] # DEBUG
        #self._mcp_configs: dict = json.loads(mcpConfigPath.read_text(encoding="utf-8"))["mcpServers"]

        self._mcp_tools: list[McpTool] = []


    @property
    def tools(self) -> Sequence[CallableTool]:
        self._log.debug("McpServerManager.tools:") # DEBUG
        for mt in self._mcp_tools: # DEBUG
            self._log.debug(f"\t{mt.routing_name}") # DEBUG

        tools_copy = copy(self._mcp_tools)

        self._log.debug("McpServerManager.tools copy:") # DEBUG
        for ct in tools_copy: # DEBUG
            self._log.debug(f"\t{ct.routing_name}") # DEBUG

        return tools_copy


    def _generate_tool_schema(self, tool) -> dict:
        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema,
            },
        }

    def _get_server_params_from_spec(self, spec: dict) -> StdioServerParameters:
        return StdioServerParameters(command=spec["command"], args=spec["args"])


    async def start_server(self, params: StdioServerParameters) -> ClientSession:
        """Launch an MCP server process in an async context."""
        read, write = await self._stack.enter_async_context(stdio_client(params))
        session = await self._stack.enter_async_context(ClientSession(read, write))
        await session.initialize()
        return session


    async def launch_servers(self) -> None:
        """Read in mcpServers.json config, fetch tool schemas, and launch each MCP server."""

        if len(self._mcp_configs) < 1:
            self._log.warn("WARNING: mcpServers.json is empty.")

        for routing_name, spec in self._mcp_configs.items():
            params = self._get_server_params_from_spec(spec)

            # Start the MCP server and capture its session instance.
            try:
                session = await self.start_server(params)
            except Exception as ex:
                self._log.error(f"ERROR: launch_servers() failed to start '{routing_name}'\n{ex}")
                continue

            # Gather tool schemas from each MCP server process.
            try:
                # TODO: Tap into session's tool pagination with `cursor=` parameter.
                list_tools_result = (await session.list_tools())
                new_tools = list_tools_result.tools

            except Exception as ex:
                self._log.error(f"ERROR: session.list_tools() failed: '{routing_name}'\n{ex}")
                continue

            # Build the McpTools
            for tool in new_tools:
                schema = self._generate_tool_schema(tool)
                self._mcp_tools.append(McpTool(routing_name, schema, session))

            self._log.info(f"MCP connected '{routing_name}': {[tl.name for tl in new_tools]}")
