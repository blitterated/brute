import subprocess

_KEY_PATH = "API/oMLX/api_key"

def get_key() -> str:
    try:
        result = subprocess.run(
            ["gopass", "show", "-o", _KEY_PATH],
            capture_output=True,
            text=True,
            check=True
        )

        api_key = result.stdout.strip()
        return api_key

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"gopass failed for '{_KEY_PATH}': {e.stderr.strip()}")
