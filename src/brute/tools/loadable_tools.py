from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from .callable_tool import CallableTool


#@runtime_checkable # <-- Enables usage of isinstance(tool, CallableTool)
class LoadableTools(Protocol):
    @property
    def tools(self) -> Sequence[CallableTool]: ...
