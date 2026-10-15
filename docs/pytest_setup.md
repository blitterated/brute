# pytest Setup

## Add pytest to uv based project

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


## Imports

### AI writeup

To configure import behavior in `pyproject.toml`, use the `[tool.pytest.ini_options]` section to set `pythonpath` for module discovery and `addopts` with `--import-mode=importlib` for isolated imports. [^gh12016]

```toml
[tool.pytest.ini_options]
# Add the source directory to the Python path
pythonpath = ["src"]

# Use importlib mode to avoid namespace pollution and handle relative imports correctly
addopts = ["--import-mode=importlib"]
```

__Key Configuration Options:__

* `pythonpath`: Specifies directories (e.g., `["src"]`) to add to `sys.path` so pytest can import your application code. This is essential for the `src` layout. [^pytestgoodpractices] [^lucasmelincfg]
* `--import-mode=importlib`: Recommended for new projects; it imports modules using `importlib` rather than the default `prepend`, which helps avoid import errors and namespace collisions, especially with relative imports in nested packages.
* `testpaths`: Defines which directories contain tests (e.g., `["tests"]`), though this is separate from import configuration. [^bitecode]

If you encounter `ImportError: attempted relative import with no known parent package`, ensure you are using `--import-mode=importlib` and that your `pythonpath` correctly points to the root of the package hierarchy.


[^gh12016]: [Add mode to only autodiscover paths with pyproject.toml or setup.py #12016](https://github.com/pytest-dev/pytest/issues/12016)
[^pytestgoodpractices]: [pytest: Good Integration Practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html)
[^lucasmelincfg]: [Lucas Melin: Configuring the pytest import mechanism via pyproject](https://lucasmelin.com/blog/2025/Dec/22/pytest-pyproject/)
[^bitecode]: [bitecode: Testing with Python (part 3): pytest setup]()



