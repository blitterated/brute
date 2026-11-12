import pytest

from pathlib import Path

from brute.logging import Loggable
from brute.logging import StdErrLogger


@pytest.fixture()
def std_err_logger() -> Loggable:
    """Create and return a logger that dumps to STDERR."""
    return StdErrLogger()
