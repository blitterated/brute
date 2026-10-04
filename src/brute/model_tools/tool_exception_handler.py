import functools
import sys

def tool_exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except Exception as ex:
            err_msg = f"Error in {func.__name__}:\n{ex}"
            print(err_msg, file=sys.stderr)
            return err_msg

    return wrapper
