import pytest

from dataclasses import dataclass


@dataclass
class ExpectedFile:
    path:    str
    name:    str
    full_path:     str
    content: str


@pytest.fixture()
def generate_expected_file(tmp_path: pathlib.Path) -> Callable[[str, bool], ExpectedFile]:
    """Return a factory function for creating test files for model tools."""
    def generate(filename: str, create: bool = True):
        """Create metadata for a markdown test file, optionally create the file, and return the metadata in an ExpectedFile."""
        file_content = f"I\nam\na\nhappy\nlittle\n{filename}"
        test_file = tmp_path / filename

        if (create):
            test_file.write_text(file_content, encoding="utf-8")

        return ExpectedFile(path=str(tmp_path),
                            name=filename,
                            full_path=str(test_file),
                            content=file_content)

    return generate
