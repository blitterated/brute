import os
import pytest
import random
import re

import brute.secrets.api_key as api_key


def test_get_key_from_env(monkeypatch):
    # Arrange
    rnd_env_var_name = f"OMLX_API_KEY_{''.join(random.choices('0123456789ABCDEF', k=16))}"
    expected_secret = "password123"
    missing_key_default = "***N0t@K3y***"

    # Arrange: use the randomized env var name
    monkeypatch.setattr(api_key, 'DEFAULT_KEY_ENV_VAR', rnd_env_var_name)

    # Arrange: Write out the test value.
    os.environ[rnd_env_var_name] = expected_secret

    # Act
    found_secret = api_key.get_key()

    # Assert
    assert(found_secret == expected_secret)

    # Teardown the env var
    del os.environ[rnd_env_var_name]


def test_get_key_with_subproc_command(monkeypatch):
    expected_secret = "password123"

    test_key = "api/give/secrets/now"

    # Just regurgitate the expected_secret from the shell.
    # The default subproc command calls out to gopass
    test_subproc_command = ['python3', '-c', 'import sys; print(sys.argv[1])', expected_secret]

    monkeypatch.setattr(api_key, 'DEFAULT_KEY_PATH', test_key)
    monkeypatch.setattr(api_key, 'DEFAULT_SUBPROC_COMMAND', test_subproc_command)

    found_secret = api_key.get_key()

    assert found_secret == expected_secret


def test_get_key_throws_ex_with_bad_key(monkeypatch):
    bad_key = "/i/am/a/bad/key"
    expected_msg = f"gopass failed for '{bad_key}'"

    monkeypatch.setattr(api_key, 'DEFAULT_KEY_PATH', bad_key)

    with pytest.raises(RuntimeError, match=re.escape(expected_msg)):
        api_key.get_key()
