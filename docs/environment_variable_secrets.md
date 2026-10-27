# Environment Variable Secrets with uv

## Quick Workarounds

### Alias uv

Run this in the project directory or source it from an rc file.

```sh
alias uvrun="uv run --env-file .env "
```

### Set and export UV_ENV_FILE

Run this in the project directory or source it from an rc file.

```sh
export UV_ENV_FILE='.env'
```


## File contents

### `.env`

```text
OMLX_API_KEY=omlx-zyn2t8os5p3m5ewg
OMLX_API_KEY=omlx-g0F1nDy0uR0wnK3y
```

### `read_env.py`

This is a basic script that checks if the secret is available or not.

```python
import os

env_var_not_found = "<eol type='sark'>END OF LINE, PROGRAM</eol>"

api_key = os.getenv("OMLX_API_KEY", env_var_not_found)

if (api_key == env_var_not_found):
    print("DENIED INTELLIGENCE AUGMENTATION")
else:
    print(f"{api_key =}")
```


### `UV_ENV_FILE.sh`

This file exports the `UV_ENV_FILE` environment variable pointing to the `.env` file.
The `.env` file stores the secret, and `uv run` will load it into the environment.

```sh
# Source this file in a shell in the root of the project like so:
#   source ./UV_ENV_FILE.sh

export UV_ENV_FILE=".env"
```


## Testing

### Using `uv`'s `--env-file`

I get denied without the `--env-file` option.

```sh
uv run read_env.py
```

```text
DENIED INTELLIGENCE AUGMENTATION
```

I get approved when I use the `--env-file` option.

```sh
uv run --env-file .env read_env.py
```

```text
api_key ='omlx-zyn2t8os5p3m5ewg'
```

I get denied again by removing the `--env-file` option.

```text
uv run read_env.py
```

```text
DENIED INTELLIGENCE AUGMENTATION
```


### Using UV_ENV_FILE and an ".env" file

The `UV_ENV_FILE.sh` file exports the `UV_ENV_FILE` environment variable which points at an `.env` file.
The `.env` file stores the secret, and `uv run` will load it into the environment.

First, without `UV_ENV_FILE`:

```sh
uv run read_env.py
```

```text
DENIED INTELLIGENCE AUGMENTATION
```

Now, with `UV_ENV_FILE`:
```sh
source UV_ENV_FILE.sh
uv run read_env.py
```

```text
api_key ='omlx-zyn2t8os5p3m5ewg'
```

## References

### Astral documentation for UV_ENV_FILE

[Astral docs -> Environment variables -> UV_ENV_FILE](https://docs.astral.sh/uv/reference/environment/#uv_env_file)

> __`UV_ENV_FILE`__
> `.env` files from which to load environment variables when executing `uv run` commands.


### uv GitHub Issue #15714

This issue is still open. There's no config file equivalent of `UV_ENV_FILE`.

[Allow setting .env file path in pyproject.toml or self-contained script front-matter](https://github.com/astral-sh/uv/issues/15714)
