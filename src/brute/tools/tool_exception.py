class ToolException(Exception):
    """The model tool specific Exception. Think of it as an envelope for other exceptions."""

class ToolCommandException(ToolException):
    """The model tool run command specific Exception."""
