import functools
import sys

class ModelToolException(Exception):
    """The model tool specific Exception. Think of it as an envelope for other exceptions."""


def tool_exception_handler(func):
    """Decorator handling exception handling for model tool functions,"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except Exception as ex:
            ex_class_name = type(ex).__name__
            err_msg = f"Error in {func.__name__}: {ex_class_name}"
            raise ModelToolException(err_msg) from ex

    return wrapper
