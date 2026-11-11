import builtins
import pytest
import re

from collections.abc import Callable
from pathlib import Path

import brute.tools.builtins as btools
from brute.tools import ToolException, ToolCommandException


# list_files()

@pytest.fixture()
def expected_file_list(tmp_path: Path):
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


def test_list_files(tmp_path: Path, expected_file_list: str):
    found_file_list = btools.ListFilesTool().list_files(str(tmp_path))
    assert found_file_list == expected_file_list


@pytest.mark.asyncio
async def test_run_list_files(tmp_path: Path, expected_file_list: str):
    found_file_list = await btools.ListFilesTool().run({ "path": str(tmp_path) })
    assert found_file_list == expected_file_list


def test_list_files_throws_ex_with_bad_path():
    bad_path = "/i/am/not/a/real/file/path/"
    expected_msg = "Error in tool: list_files: FileNotFoundError"
    with pytest.raises(ToolException, match=re.escape(expected_msg)):
        btools.ListFilesTool().list_files(bad_path)


# read_file()

def test_read_file(generate_expected_file: Callable[[str, bool], ExpectedFile]):
    expected_file = generate_expected_file(filename="monkey")
    found_file_content = btools.ReadFileTool().read_file(expected_file.full_path)
    assert found_file_content == expected_file.content


@pytest.mark.asyncio
async def test_run_read_files(generate_expected_file: Callable[[str, bool], ExpectedFile]):
    expected_file = generate_expected_file(filename="monkey")
    found_file_content = await btools.ReadFileTool().run({ "path": expected_file.full_path })
    assert found_file_content == expected_file.content


def test_read_file_throws_ex_with_bad_path():
    bad_path = "/i/am/not/a/real/file/path/platypus.md"
    expected_msg = "Error in tool: read_file: FileNotFoundError"
    with pytest.raises(ToolException, match=re.escape(expected_msg)):
        btools.ReadFileTool().read_file(bad_path)


# write_file()


def test_write_file(generate_expected_file: ExpectedFile):
    expected_file = generate_expected_file(filename="turnip", create=False)
    expected_response = f"Saved {expected_file.full_path} ({len (expected_file.content)} characters)"

    found_response = btools.WriteFileTool().write_file(expected_file.full_path, expected_file.content)
    # read_file() is basic enough that we can use it here instead of copying its code.
    found_file_content = btools.ReadFileTool().read_file(expected_file.full_path)

    assert found_response == expected_response
    assert found_file_content == expected_file.content


@pytest.mark.asyncio
async def test_run_write_file(generate_expected_file: ExpectedFile):
    expected_file = generate_expected_file(filename="turnip", create=False)
    expected_response = f"Saved {expected_file.full_path} ({len (expected_file.content)} characters)"

    tool_args = {
        "path": expected_file.full_path,
        "content": expected_file.content,
    }

    found_response = await btools.WriteFileTool().run(tool_args)
    # read_file() is basic enough that we can use it here instead of copying its code.
    found_file_content = btools.ReadFileTool().read_file(expected_file.full_path)

    assert found_response == expected_response
    assert found_file_content == expected_file.content


def test_write_file_throws_ex_with_bad_path():
    bad_path = "/i/am/not/a/real/file/path/platypus.md"
    expected_msg = "Error in tool: write_file: FileNotFoundError"
    with pytest.raises(ToolException, match=re.escape(expected_msg)):
        btools.WriteFileTool().write_file(bad_path, "Lorem impsum")


# run_command()

@pytest.fixture()
def user_always_says_yes(monkeypatch):
    monkeypatch.setattr(builtins, 'input', lambda _: "y")


@pytest.fixture()
def user_always_says_no(monkeypatch):
    monkeypatch.setattr(builtins, 'input', lambda _: "n")


def test_run_command_stdout(user_always_says_yes):
    expected_cmd_stdout = "testing... 1, 2, 3... testing..."
    found_cmd_stdout = btools.RunCommandTool().run_command(f"echo \"{expected_cmd_stdout}\"")
    assert found_cmd_stdout == expected_cmd_stdout


def test_run_command_stderr(user_always_says_yes):
    expected_cmd_stderr = "... --- ...   ... --- ..."
    found_cmd_stderr = btools.RunCommandTool().run_command(f"1>&2 echo \"{expected_cmd_stderr}\"")
    assert found_cmd_stderr == expected_cmd_stderr


def test_run_command_no_output(user_always_says_yes):
    expected_cmd_no_output = "(no output, exit code 0)"
    found_cmd_output = btools.RunCommandTool().run_command(":")
    assert found_cmd_output == expected_cmd_no_output


def test_run_command_user_refuses(user_always_says_no):
    expected_cmd_output = "The user declined to run this command."
    found_cmd_output = btools.RunCommandTool().run_command(":")
    assert found_cmd_output == expected_cmd_output


@pytest.mark.asyncio
async def test_run_run_command(user_always_says_yes):
    expected_cmd_stdout = "testing... 1, 2, 3... testing..."

    tool_name = "run_command"
    tool_args = {"command": f"echo \"{expected_cmd_stdout}\""}

    found_cmd_stdout = await btools.RunCommandTool().run(tool_args)
    assert found_cmd_stdout == expected_cmd_stdout


def test_run_command_throws_ex_with_bad_command(user_always_says_yes):
    bad_command = "/sark/tron"
    outer_expected_msg = "Error in tool: run_command: ToolCommandException"
    inner_expected_msg = "run_command() returned a non-zero exit code: 127\n\n/bin/sh: /sark/tron: No such file or directory"

    with pytest.raises(ToolException) as ex_info:
        btools.RunCommandTool().run_command(bad_command)

    outer_ex = ex_info.value
    inner_ex = ex_info.value.__cause__

    assert outer_expected_msg in str(outer_ex)
    assert inner_ex is not None
    assert type(inner_ex) is ToolCommandException
    assert inner_expected_msg in str(inner_ex)
