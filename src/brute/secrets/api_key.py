from pprint import pprint

import subprocess


DEFAULT_KEY_PATH = "API/oMLX/api_key"

DEFAULT_SUBPROC_COMMAND = ["gopass", "show", "-o"]


def get_key() -> str:
    key_path: str = DEFAULT_KEY_PATH
    subproc_cmd: list[str] = [*DEFAULT_SUBPROC_COMMAND]
    subproc_cmd.append(key_path)

    print(f"get_key(): subproc_cmd: {' '.join(subproc_cmd)}") # DEBUG

    try:
        result = subprocess.run(
            subproc_cmd,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"get_key(): result:") # DEBUG
        pprint(vars(result)) # DEBUG

        std_err = result.stderr.strip() # DEBUG
        print(f"{std_err =}") # DEBUG

        api_key = result.stdout.strip()
        print(f"{api_key =}") # DEBUG

        return api_key

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"gopass failed for '{DEFAULT_KEY_PATH}': {e.stderr.strip()}")
