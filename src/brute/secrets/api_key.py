import os
import subprocess

from dataclasses import dataclass
from pprint import pprint


DEFAULT_KEY_PATH = "API/oMLX/api_key"
DEFAULT_KEY_ENV_VAR= "OMLX_API_KEY"

DEFAULT_SUBPROC_COMMAND = ["gopass", "show", "-o"]


@dataclass
class KeyResult:
    success: bool = False
    api_key: str  = ""


def _get_key_from_env():
    api_key = os.getenv(DEFAULT_KEY_ENV_VAR)

    if (api_key == None):
        return KeyResult(success=False)
    else:
        return KeyResult(success=True, api_key=api_key)


def _get_key_from_gopass() -> str:
    subproc_cmd: list[str] = [*DEFAULT_SUBPROC_COMMAND]
    subproc_cmd.append(DEFAULT_KEY_PATH)

    try:
        result = subprocess.run(
            subproc_cmd,
            capture_output=True,
            text=True,
            check=True
        )
        api_key = result.stdout.strip()

        return api_key

    except subprocess.CalledProcessError as ex:
        raise RuntimeError(f"gopass failed for '{DEFAULT_KEY_PATH}': {ex.stderr.strip()}") from ex


def get_key() -> str:
    key_result = _get_key_from_env()
    if (key_result.success):
        return key_result.api_key

    return _get_key_from_gopass()
