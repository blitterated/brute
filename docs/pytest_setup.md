# pytest Setup

Add pytest as a dev dependeny.

```sh
uv add pytest --dev
```

```text
Resolved 22 packages in 275ms
      Built brute @ file:///Users/pete/Development/blitterated/brute/src                                                                Prepared 6 packages in 153ms                                                                                                            Uninstalled 1 package in 1ms                                                                                                            Installed 6 packages in 5ms                                                                                                              ~ brute==0.1.0 (from file:///Users/pete/Development/blitterated/brute/src)                                                              + iniconfig==2.3.0
 + packaging==26.3
 + pluggy==1.6.0
 + pygments==2.21.0
 + pytest==9.1.1
```


Take a look at the resulting config.

```sh
bat -p pyproject.toml
```

```text
[project]
name = "brute"
version = "0.1.0"
description = "Rude and mental harness. Not a gent, a brute."
authors = [
    { name = "blitterated", email = "blitterated@proton.me" }
]
requires-python = ">=3.14"
dependencies = [
    "openai>=3.19.2",
]

[project.scripts]
brute = "brute:main"

[build-system]
requires = ["uv_build>=0.12.19,<0.13.0"]
build-backend = "uv_build"

[dependency-groups]
dev = [
    "pytest>=9.1.1",
]
```


Prepare the tests director.

```sh
mkdir tests
touch tests/__init__.py
```


Smoke test pytest.

```sh
uv run pytest
```

```text
========================================================= test session starts ==========================================================
platform darwin -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/pete/Development/blitterated/brute/src
configfile: pyproject.toml
plugins: anyio-4.15.1
collected 0 items

======================================================== no tests ran in 0.01s =========================================================
```
