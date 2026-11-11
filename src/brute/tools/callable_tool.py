import functools

from typing import Protocol, runtime_checkable

from .tool_exception import ToolException


@runtime_checkable # <-- Enables usage of isinstance(tool, CallableTool)
class CallableTool(Protocol):
    @property
    def routing_name(self) -> str: ...


    @property
    def schema(self) -> dict: ...


    async def run(self, args: dict) -> str: ...


    @staticmethod
    def tool_exception_handler(func):
        """Exception handling decorator for tool call implementations."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except Exception as ex:
                ex_class_name = type(ex).__name__
                err_msg = f"Error in tool: {func.__name__}: {ex_class_name}"
                raise ToolException(err_msg) from ex

        return wrapper
