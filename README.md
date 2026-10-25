# brute

_A brute, not a gent._

This is a simple agent harness.


## Features

* Agentic loop
* Uses OpenAI API
* Tool calls to python functions in brute source code:
    * list files
    * read files
    * write files
    * run commands
* Speaks `gopass` for secret management


## Side Quest

Experiment with classless Python programming. It leans heavy on modules and packages for encapsulation.

The runtime code uses `__init__.py` like OOP interfaces. When runtime code imports via `__init__.py`, things like module level variables and constants can be left out.

However, tests can import files directly to access and monkeypatch module items that are ignored by `__init__.py`.

For example, `secrets/api_key.py` contains a couple of module level constants: `DEFAULT_KEY_PATH` and `DEFAULT_SUBPROC_COMMAND`.
Neither are imported in `secrets/__init__.py`. The only explicit import in there is `from .api_key import get_key`.
This signals to anyone developing code using `import brute.secrets as api` that the constants are "off limits", but that `get_key()` is in play.

The hierarchy of `__init__.py` files can be seen as a filter for module code not intended to be "public".

When brute is started, the top level `__init__.py` imports `model_client` as `client` and `model_tools` as `tools`.


```python
import brute.model_client as client
import brute.model_tools as tools
```

This effectively exposes anything imported in those modules' `__init__.py` files as functions or properties of `client` and `tools`.

For example:

```python
import brute

TOOL_SCHEMAS = brute.tools.SCHEMAS
result = brute.tools.run(tool_name, tool_args)
client = brute.client.create()
```
