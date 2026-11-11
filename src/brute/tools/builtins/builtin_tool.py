import functools
import sys

from abc import ABC, abstractmethod

from ..callable_tool import CallableTool
from .builtin_tool_exception import BuiltinToolException


class BuiltinTool(ABC, CallableTool):
    @property
    @abstractmethod
    def routing_name(self) -> str: pass


    @property
    @abstractmethod
    def schema(self) -> dict: pass


    @abstractmethod
    async def run(self, args: dict) -> str: pass
