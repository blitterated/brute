import pytest


@pytest.fixture()
def import_debug_info():
    def inner_func():
        debug_info = [f"import_debug_info: __name__    = {__name__}"]

        pkg_name = None
        match __package__:
            case None:
                pkg_name = "None"
            case "":
                pkg_name = "(empty string)"
            case _:
                pkg_name = __package__

        debug_info.append(f"import_debug_info: __package__ = {pkg_name}")

        return "\n".join(debug_info)

    return inner_func
