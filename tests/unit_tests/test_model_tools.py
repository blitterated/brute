import pathlib

import brute.model_tools.list_files as lf
import brute.model_tools.read_file as rf
import brute.model_tools.write_file as wf
import brute.model_tools.run_command as rc


def setup_list_files_files(a_temp_path: pathlib.Path):
    test_file = a_temp_path / "one.md"
    test_file.write_text("# One", encoding="utf-8")

    test_file = a_temp_path / "two.md"
    test_file.write_text("## Two\n\n## Two", encoding="utf-8")

    test_file = a_temp_path / "three.md"
    test_file.write_text("### Three\n\n### Three\n\n### Three", encoding="utf-8")


def test_list_files_can_list_files(tmp_path):
    # Arrange
    setup_list_files_files(tmp_path)

    # Act
    files = lf.list_files(tmp_path)

    # Assert
    assert files == 'one.md\nthree.md\ntwo.md'
