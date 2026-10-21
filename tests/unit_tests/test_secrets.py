import pytest

import brute.secrets.api_key as api_key


def test_get_key(monkeypatch):
    expected_secret = "password123"

    test_key_path = "api/give/secrets/now"

    # Just regurgitate the expected_secret from the shell.
    #test_subproc_command = ["echo", expected_secret]
    #test_subproc_command = ['_()', '{', 'echo' '"$1"', '}' '&&', '_', expected_secret]
    #test_subproc_command = [f"_() {{ echo $1 }} && _ {expected_secret}"]
    #test_subproc_command = [f"eval '_() {{ echo $1 }}'", "&&", "_" "{expected_secret}"]
    #test_subproc_command = [f"eval", '_() {{ echo $1 }}', "&&", "_" "{expected_secret}"]
    #test_subproc_command = ['python3', '-c', '"import sys; print(sys.argv[1])"', expected_secret]
    #test_subproc_command = ['python3', '-c', '"import sys, time; time.sleep(1); print(sys.argv[1])"', expected_secret]
    #test_subproc_command = ["gawk", "BEGIN { print ARGV[1] }", expected_secret]
    test_subproc_command = ['python3', '-c', 'import sys; print(sys.argv[1])', expected_secret]

    cmd_hack = " ".join(test_subproc_command) # DEBUG
    print(f"test_get_key(): {cmd_hack}") # DEBUG

    monkeypatch.setattr(api_key, 'DEFAULT_KEY_PATH', test_key_path)
    monkeypatch.setattr(api_key, 'DEFAULT_SUBPROC_COMMAND', test_subproc_command)

    found_secret = api_key.get_key()

    assert found_secret == expected_secret



#def test_get_key_throws_ex_with_bad_key_path():
#    bad_path = "/i/am/not/a/real/file/path/"
#    expected_msg = "Error in brute.model_tools.list_files(): FileNotFoundError"
#    with pytest.raises(mtools.ModelToolException, match=re.escape(expected_msg)):
#        mtools.list_files(bad_path)
