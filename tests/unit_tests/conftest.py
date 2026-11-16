import json
import pytest

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Unpack


@dataclass
class ExpectedFile:
    path:    str
    name:    str
    full_path:     str
    content: str


@pytest.fixture()
def generate_expected_file(tmp_path: Path) -> Callable[[str, bool], ExpectedFile]:
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


@pytest.fixture()
def mcpTestConfigFile(
    tmp_path: Path,
    mcpTestConfig: Callable[[str], dict[str, dict]]
) -> Callable[[str], Path]:
    """
    Generate and return an mcpServers.json file for testing purposes.

    This file is used by brute to identify and run MCP servers.
    In this case, it is just a simple string reversing MCP server.
    """
    def generate(routing_name: str) -> Path:
        mcpTestConfigContent = json.dumps(mcpTestConfig(routing_name))
        mcpTestConfigFile = tmp_path / "mcpServers.json"
        mcpTestConfigFile.write_text(mcpTestConfigContent, encoding="utf-8")
        return mcpTestConfigFile

    return generate


@pytest.fixture()
def mcpTestConfig() -> Callable[[str], dict[str, dict]]:
    """
    Generate and return multiple MCP server configurations for
    an mcpServers.json file to be used during testing.

    They're separate instances of the same MCP server (reverse)
    but with a different routing name.
    """
    def generate(*routing_names: str) -> dict[str, dict]:
        """Create config for an mcpServers.json config file."""
        mcpServerConfigs: dict[str, dict] = { "mcpServers": {} }

        for rtname in routing_names:
            mcpServerConfigs["mcpServers"][rtname] = {
                "command": "uv",
                "args": [ "run", "tests/unit_tests/stdio_mcp_test_server.py" ]
            }

        return mcpServerConfigs

    return generate
