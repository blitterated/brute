import brute.model_tools.list_files as list_files
import brute.model_tools.read_file as read_file
import brute.model_tools.write_file as write_file
import brute.model_tools.run_command as run_command

def test_list_files_can_list_files():
    assert list_files.list_files() == "foo"
