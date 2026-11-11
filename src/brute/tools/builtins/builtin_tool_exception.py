class BuiltinToolException(Exception):
    """The model tool specific Exception. Think of it as an envelope for other exceptions."""

class BuiltinToolCommandException(BuiltinToolException):
    """The model tool run command specific Exception."""
