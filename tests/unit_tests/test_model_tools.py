import brute.model_tools.list_files as lf
import brute.model_tools.read_file as rf
import brute.model_tools.write_file as wf
import brute.model_tools.run_command as rc


def test_list_files_can_list_files(test_dir_path):
    print(f"test_list_files_can_list_files(): test_dir_path: {test_dir_path}") # DEBUG

    files = lf.list_files().encode("unicode_escape").decode("utf-8")
    print(f"test_list_files_can_list_files(): files:\n{files}") # DEBUG

#    assert lf.list_files() == "foo"
