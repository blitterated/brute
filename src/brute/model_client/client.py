from openai import OpenAI

import brute.secrets as api


def create():
    client = OpenAI(
        base_url="http://127.0.0.1:8000/v1",
        api_key=api.get_key(),
    )
