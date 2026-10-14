import os
import pytest

@pytest.fixture()
def test_dir_path():
    cwd = os.getcwd()
    print(f"\ntest_dir_path(): cwd = '{cwd}'")
