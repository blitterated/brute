import pathlib

import brute.model_tools.list_files as lf
import brute.model_tools.read_file as rf
import brute.model_tools.write_file as wf
import brute.model_tools.run_command as rc


def setup_list_files_files(a_temp_path: pathlib.Path):
    print(f"\nsetup_list_files_files(): a_temp_path = '{a_temp_path}'") # DEBUG

    test_file = a_temp_path / "one.md"
    test_file.write_text("# One", encoding="utf-8")

    test_file = a_temp_path / "two.md"
    test_file.write_text("## Two\n\n## Two", encoding="utf-8")

    test_file = a_temp_path / "three.md"
    test_file.write_text("### Three\n\n### Three\n\n### Three", encoding="utf-8")


def test_list_files_can_list_files(tmp_path, test_dir_path):
    print(f"test_list_files_can_list_files(): test_dir_path: {test_dir_path}") # DEBUG

    # Arrange
    setup_list_files_files(tmp_path)

    # Act
    files = lf.list_files(tmp_path)
    print(f"test_list_files_can_list_files(): files:\n{files}") # DEBUG
    print(f"raw files string: {repr(files)}")

    # Assert
    assert files == 'one.md\nthree.md\ntwo.md'
