import pathlib
import pytest
import re

import brute.model_tools as mtools


# list_files()

@pytest.fixture()
def expected_file_list(tmp_path: pathlib.Path):
    """Create three markdown test files, and return a list of filenames."""
    file_words = ["one", "two", "three"]
    file_names = []

    for fw in file_words:
        filename = f"{fw}.md"
        file_names.append(filename)
        file_content = f"# Markdown File {fw.capitalize()}"
        test_file = tmp_path / filename
        test_file.write_text(file_content, encoding="utf-8")

    return "\n".join(sorted(file_names))


def test_list_files(tmp_path: pathlib.Path, expected_file_list: str):
    found_file_list = mtools.list_files(str(tmp_path))
    assert found_file_list == expected_file_list


def test_list_files_throws_ex_with_bad_path():
    bad_path = "/i/am/not/a/real/file/path/"
    expected_msg = "Error in brute.model_tools.list_files(): FileNotFoundError"
    with pytest.raises(mtools.ModelToolException, match=re.escape(expected_msg)):
        mtools.list_files(bad_path)


# read_file()

def test_read_file(tmp_path):
    filename = "monkey.md"
    expected_file_content = "I\nam\na\nhappy\nlittle\nmonkey"
    test_file = tmp_path / filename
    test_file.write_text(expected_file_content, encoding="utf-8")
    found_file_content = mtools.read_file(tmp_path / filename)
    assert found_file_content == expected_file_content


def test_read_file_throws_ex_with_bad_path():
    bad_path = "/i/am/not/a/real/file/path/platypus.md"
    expected_msg = "Error in brute.model_tools.read_file(): FileNotFoundError"
    with pytest.raises(mtools.ModelToolException, match=re.escape(expected_msg)):
        mtools.read_file(bad_path)


# write_file()

def test_write_file(tmp_path):
    filename = "turnip.md"
    expected_file_content = "I\nam\na\nhappy\nlittle\nturnip"
    test_file = tmp_path / filename

    mtools.write_file(test_file, expected_file_content)

    # read_file() is basic enough that we can use it here instead of copying its code.
    found_file_content = mtools.read_file(test_file)
    assert found_file_content == expected_file_content


def test_write_file_throws_ex_with_bad_path():
    bad_path = "/i/am/not/a/real/file/path/platypus.md"
    expected_msg = "Error in brute.model_tools.write_file(): AttributeError"
    with pytest.raises(mtools.ModelToolException, match=re.escape(expected_msg)):
        mtools.write_file(bad_path, "Lorem impsum")
