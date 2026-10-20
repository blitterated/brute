import subprocess

DEFAULT_KEY_PATH = "API/oMLX/api_key"

DEFAULT_SUBPROC_COMMAND = ["gopass", "show", "-o"]


def get_key(key_path: str = DEFAULT_KEY_PATH,
            subproc_cmd: list[str] = [*DEFAULT_SUBPROC_COMMAND]) -> str:

    subproc_cmd.append(key_path)

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
        raise RuntimeError(f"gopass failed for '{DEFAULT_KEY_PATH}': {e.stderr.strip()}")
