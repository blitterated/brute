import brute.model_tools.list_files as lf
import brute.model_tools.read_file as rf
import brute.model_tools.write_file as wf
import brute.model_tools.run_command as rc


print(f"\ntest_model_tools.py: __name__    = {__name__}")

pkg_name = None
match __package__:
    case None:
        pkg_name = "None"
    case "":
        pkg_name = "(empty string)"
    case _:
        pkg_name = __package__

print(f"test_model_tools.py: __package__ = {pkg_name}")


def test_import_debug_info(import_debug_info):
    print(f"import_debug_info:\n{import_debug_info}\n")
    pass


def test_list_files_can_list_files(test_dir_path):
    print(f"test_list_files_can_list_files(): test_dir_path: {test_dir_path}")

    files = lf.list_files().encode("unicode_escape").decode("utf-8")
    print(f"test_list_files_can_list_files(): files:\n{files}")

#    assert lf.list_files() == "foo"
