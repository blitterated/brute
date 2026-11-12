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




from inspect import getmembers





class McpServerManager(LoadableTools):
    # Project Paths config
    #_projectRoot = Path(__file__).parent
    #_mcpConfig = _projectRoot / "mcp_servers.json"


    def __init__(self, stack: AsyncExitStack, mcpConfigPath: Path, log: Loggable):
        self._stack: AsyncExitStack = stack
        self._mcp_configs: dict = json.loads(mcpConfigPath.read_text(encoding="utf-8"))["mcpServers"]
        self._log: Loggable = log

        self._mcp_tools: list[McpTool] = []

        self._log.debug(f"McpServerManager.init(): _mcp_configs:\n\t{json.dumps(self._mcp_configs)}") # DEBUG


    @property
    def tools(self) -> Sequence[CallableTool]:
        return copy(self._mcp_tools)


    def _generate_tool_schema(self, tool) -> dict:

        self._log.debug(f"McpServerManager._generate_tool_schema(): tool class: \"{type(tool).__name__}\"") # DEBUG

        for mbr_name, mbr_val in tool:
            self._log.debug(f"\ttool members: {mbr_name}: {mbr_val}") # DEBUG


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

        self._log.debug(f"McpServerManager.start_server(): Creating client session") # DEBUG

        read, write = await self._stack.enter_async_context(stdio_client(params))
        session = await self._stack.enter_async_context(ClientSession(read, write))
        await session.initialize()

        self._log.debug(f"McpServerManager.start_server(): Client session created") # DEBUG

        return session


    async def launch_servers(self) -> None:
        """Read in mcpServers.json config, fetch tool schemas, and launch each MCP server."""

        if len(self._mcp_configs) < 1:
            self._log.warn("WARNING: mcpServers.json is empty.")

        for routing_name, spec in self._mcp_configs.items():
            params = self._get_server_params_from_spec(spec)
            self._log.debug(f"McpServerManager.launch_servers(): params class: \"{type(params).__name__}\"") # DEBUG
            self._log.debug(f"McpServerManager.launch_servers(): Created params for \"{routing_name}\"") # DEBUG
            self._log.debug(f"McpServerManager.launch_servers(): spec:\n\t\"{spec}\"") # DEBUG

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

                self._log.debug(f"McpServerManager.launch_servers(): list_tools_result module: \"{type(list_tools_result).__module__}\"") # DEBUG
                self._log.debug(f"McpServerManager.launch_servers(): list_tools_result class: \"{type(list_tools_result).__name__}\"") # DEBUG


#                ltr_members = getmembers(type(list_tools_result)) # DEBUG
#                for name, _ in ltr_members:
#                    self._log.debug(f"\t{name}") # DEBUG

                new_tools = list_tools_result.tools

                self._log.debug(f"McpServerManager.launch_servers(): mcp_tools count: {len(new_tools)}") # DEBUG

            except Exception as ex:
                self._log.error(f"ERROR: session.list_tools() failed: '{routing_name}'\n{ex}")
                continue

            # Build the McpTools
            for tool in new_tools:
                schema = self._generate_tool_schema(tool)
                self._mcp_tools.append(McpTool(routing_name, schema, session))

                self._log.debug(f"McpServerManager.launch_servers(): \"{routing_name}\" tool schema:\n{json.dumps(schema)}") # DEBUG
                self._log.debug(f"McpServerManager.launch_servers(): _mcp_tools count: {len(self._mcp_tools)}") # DEBUG

            self._log.info(f"MCP connected '{routing_name}': {[tl.name for tl in new_tools]}")
