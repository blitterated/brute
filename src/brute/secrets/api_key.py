import subprocess

_KEY_PATH = "API/oMLX/api_key"


def _get_subproc_command(key_path: str) -> list[str]:
    cmd = ["gopass", "show", "-o"]
    cmd.append(key_path)
    return cmd


def get_key(key_path: str = _KEY_PATH) -> str:
    subproc_cmd = _get_subproc_command(key_path)

    try:
        result = subprocess.run(
            subproc_cmd,
            capture_output=True,
            text=True,
            check=True
        )

        api_key = result.stdout.strip()
        return api_key

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"gopass failed for '{_KEY_PATH}': {e.stderr.strip()}")
