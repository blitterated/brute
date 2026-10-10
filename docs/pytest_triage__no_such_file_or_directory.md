# pytest Triage - No such file or directory

## Suddenly, pytest wouldn't run

```sh
uv run pytest
```

```text
error: Failed to spawn: `pytest`
  cause: No such file or directory (os error 2)
```

Checked the project config.

```sh
bat pyproject.toml
```

```text
─────┬──────────────────────────────────────────────────────────────────────────
     │ File: pyproject.toml
     │ Size: 425 B
─────┼──────────────────────────────────────────────────────────────────────────
   1 │ [project]
   2 │ name = "brute"
   3 │ version = "0.1.0"
   4 │ description = "Rude and mental harness. Not a gent, a brute."
   5 │ authors = [
   6 │     { name = "blitterated", email = "blitterated@proton.me" }
   7 │ ]
   8 │ requires-python = ">=3.14"
   9 │ dependencies = [
  10 │     "openai>=3.19.2",
  11 │ ]
  12 │
  13 │ [project.scripts]
  14 │ brute = "brute:main"
  15 │
  16 │ [build-system]
  17 │ requires = ["uv_build>=0.12.19,<0.13.0"]
  18 │ build-backend = "uv_build"
  19 │
  20 │ [dependency-groups]
  21 │ dev = [
  22 │     "pytest>=9.1.1",
  23 │ ]
─────┴──────────────────────────────────────────────────────────────────────────
```

Tried syncing the dev dependencies.

```sh
uv sync --group dev
```

```text
Resolved 22 packages in 4ms
      Built brute @ file:///Users/pete/Development/blitterated/brute                                                                    Prepared 1 package in 4ms
Uninstalled 1 package in 0.61ms
Installed 1 package in 2ms
 ~ brute==0.1.0 (from file:///Users/pete/Development/blitterated/brute)
```

```sh
uv run pytest
```

```text
error: Failed to spawn: `pytest`
  cause: No such file or directory (os error 2)
```

Then I tried wiping and recreating the virtual environment.

```sh
uv venv --clear && uv sync
```

```text
Using CPython 3.14.7
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
Resolved 22 packages in 1ms
Installed 20 packages in 27ms
 + annotated-types==0.8.0
 + anyio==4.15.1
 + brute==0.1.0 (from file:///Users/pete/Development/blitterated/brute)
 + h11==0.16.0
 + httpcore2==2.13.1
 + httpx2==2.13.1
 + idna==3.20
 + iniconfig==2.3.0
 + jiter==0.17.0
 + openai==3.19.2
 + packaging==26.3
 + pluggy==1.6.0
 + pydantic==2.13.5
 + pydantic-core==2.46.5
 + pygments==2.21.0
 + pytest==9.1.1
 + sniffio==1.3.1
 + truststore==0.10.4
 + typing-extensions==4.16.0
 + typing-inspection==0.4.4
```

```sh
uv run pytest
```

```text
========================================================= test session starts ==========================================================
platform darwin -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/pete/Development/blitterated/brute
configfile: pyproject.toml
plugins: anyio-4.15.1
collected 0 items / 1 error

================================================================ ERRORS ================================================================
____________________________________________ ERROR collecting src/tests/test_model_tools.py ____________________________________________
ImportError while importing test module '/Users/pete/Development/blitterated/brute/src/tests/test_model_tools.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
../../../.local/share/uv/python/cpython-3.14.7-macos-aarch64-none/lib/python3.14/importlib/__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src/tests/test_model_tools.py:1: in <module>
    import brute.model_tools.list_files as list_files
src/brute/__init__.py:1: in <module>
    import model_client.client as client
E   ModuleNotFoundError: No module named 'model_client'
======================================================= short test summary info ========================================================
ERROR src/tests/test_model_tools.py
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
=========================================================== 1 error in 0.04s ===========================================================
```

Success! (If you ignore the module errors ;)


## AI repsonse to pytest error

The error `Failed to spawn: pytest` occurs because `pytest` __is not installed__ in the virtual environment that `uv run`
is using.  This typically happens when the dependency is missing from `pyproject.toml`, is placed in a dependency group
that wasn't synced, or the environment is stale.

__Common Causes and Fixes:__

* __Missing Dev Dependencies:__ pytest is often a development dependency. If it is defined in a group (e.g.,
\[dependency-groups\] dev) but you ran uv sync without including that group, it won't be installed.
  * __Fix:__ Install the specific group: `uv sync --group dev` or `uv add --dev pytest`.
* __Stale Virtual Environment:__ If you moved your project directory or the virtual environment was created without `pytest`,
`uv` may not detect the missing binary.
  * __Fix:__ Clean the environment and reinstall: `uv venv --clear && uv sync`.
* __Workspace Configuration Issues:__ In multi-package workspaces, dependencies defined in the root `pyproject.toml` might
not automatically apply to all sub-packages if not configured correctly, or `uv sync` might not install workspace member
dependencies by default.
  * __Fix:__ Ensure pytest is listed in the `pyproject.toml` of the package you are running tests in, or explicitly sync
  with `uv sync --all-packages`.
* __Using uvx vs uv run:__
  * `uv run pytest` uses the __project's__ virtual environment (requires `pytest` to be installed in the project).
  * `uvx pytest` uses an __isolated, temporary__ environment (does not require project installation, but cannot access
  project code).
  * __Fix:__ If you just want to run tests without configuring dependencies, use `uvx pytest`. If you need to test your
  project's installed code, stick with `uv run pytest` after ensuring `pytest` is in your dependencies. 

__Quick Diagnostic:__
Run `uv pip list` inside your project to see if `pytest` is actually installed. If it is not, add it using
`uv add --dev pytest` (if it's a dev tool) or `uv add pytest` (if it's a runtime dependency).

### Citations

* [fix(devcontainer): a fresh devcontainer cannot run uv run pytest #961](https://github.com/Mai0313/discordbot/issues/961)
* [Adopt uv for dev workflow: dev dependencies are undeclared and CI is unreproducible locally #8](https://github.com/qso-graph/qrz-mcp/issues/8)
* [Getting started with Python uv](https://bneijt.nl/blog/getting-started-with-python-uv/)
