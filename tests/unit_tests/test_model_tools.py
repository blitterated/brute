import pathlib
import pytest

import brute.model_tools as mtools


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
    files = mtools.list_files(tmp_path)

    # Assert
    assert files == 'one.md\nthree.md\ntwo.md'


def test_list_files_throws_ex_with_bad_path():
    # Arrange
    bad_path = "/i/am/not/a/real/file/path/"
    expected_msg = "Error in list_files: FileNotFoundError"

    # Act & Assert
    with pytest.raises(mtools.ModelToolException, match=expected_msg):
        mtools.list_files(bad_path)
