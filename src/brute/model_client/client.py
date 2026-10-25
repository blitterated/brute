from openai import OpenAI, AsyncOpenAI

import brute.secrets as api


def create():
    client = OpenAI(
        base_url="http://127.0.0.1:8000/v1",
        api_key=api.get_key(),
    )
    return client


def create_async():
    async_client = AsyncOpenAI(
        base_url="http://127.0.0.1:8000/v1",
        api_key=api.get_key(),
    )
    return async_client
