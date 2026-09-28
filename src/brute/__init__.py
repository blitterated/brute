import subprocess

from openai import OpenAI

KEY_PATH = "API/oMLX/api_key"

MODEL = "Qwen3.8-27B-8bit"

SYSTEM_PROMPT = """
You are a coding agent running in the user's terminal.
You can list files, read files, write files, and run shell commands.
Use your tools to complete the user's task, then briefly summarize what you did.
The working directory is the folder the user launched you from.
"""


def get_api_key() -> str:
    try:
        result = subprocess.run(
            ["gopass", "show", "-o", KEY_PATH],
            capture_output=True,
            text=True,
            check=True
        )

        api_key = result.stdout.strip()
        return api_key

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"gopass failed for '{KEY_PATH}': {e.stderr.strip()}")


def get_client():
    client = OpenAI(
        base_url="http://127.0.0.1:8000/v1",
        api_key=get_api_key()
    )
    return client

CLIENT = get_client()
