# Model Tool Requests

This doc captures different models' responses requesting tool calls.

Here's the prompt used to start each session:

```text
Please summarize the README.md file in the current directory
```


## Llama-3.2-3B-Instruct-8bit

```text
uv run brute
Mini agent ready. Type 'exit' to quit.

You> Please summarize the README.md file in the current directory


Bot> {"type": "function", "function": "read_file", "parameters": {"path": "README.md"}}

You> quit
```


## Qwen2.5-Coder-7B-Instruct-MLX-8bit

```text
uv run brute
Mini agent ready. Type 'exit' to quit.

You> Please summarize the README.md file in the current directory


Bot> Sure! I'll list the contents of the `README.md` file to give you an overview.

<tools>
  {"name": "list_files", "arguments": {"path": "README.md"}}
</tools>

You> quit
```


## Qwen3.5-9B-MLX-8bit

```text
uv run brute
Mini agent ready. Type 'exit' to quit.

You> Please summarize the README.md file in the current directory

Tool Call Request:
read_file({'path': 'README.md'}

Tool Call Result:
... _lots of text_

Bot> Here's a summary of the README.md file:

**Project: brute**
- A simple agent harness described as "A brute, not a gent"

**Key Concept: Classless Python Programming**
- The project experiments with avoiding traditional OOP classes
- Heavily relies on modules and packages for encapsulation
- Uses `__init__.py` files as OOP-style interfaces

**Import Hierarchy Strategy**
- `__init__.py` files act as filters for "private" vs "public" module exports
- Runtime code imports via `__init__.py` (e.g., `import brute.model_client as client`)
- Tests can import files directly to access and monkeypatch hidden items not exposed in `__init__.py`
- Example: `secrets/api_key.py` contains constants like `DEFAULT_KEY_PATH` that are intentionally not exported via `__init__.py`

**Runtime Setup**
- When brute starts, the top-level `__init__.py` imports:
  - `brute.model_client` as `client`
  - `brute.model_tools` as `tools`

In essence, this is a Python project that uses package-level imports (`__init__.py`) as a clean interface while allowing internal testing access to implementation details.

You> quit
```


## Qwen3.8-27B-8bit

```text
uv run brute
Mini agent ready. Type 'exit' to quit.

You> Please summarize the README.md file in the current directory

Tool Call Request:
list_files({'path': '.'}

Tool Call Result:
.git/
.gitignore
.pytest_cache/
.python-version
.venv/
README.md
docs/
pyproject.toml
src/
tests/
uv.lock

Tool Call Request:
read_file({'path': 'README.md'}

Tool Call Result:
... _lots of text_

Bot> Here's a summary of **README.md**:

**brute** — "A brute, not a gent" — is a simple agent harness.

The README focuses on a "Side Quest": experimenting with **classless Python programming**, where modules and packages replace classes for encapsulation:

- **`__init__.py` files act like OOP interfaces** — they define each package's public API. Runtime code imports through them, leaving internal module-level variables and constants out of the public surface.
- **Tests bypass the filter** — they can import files directly to access and monkeypatch items that `__init__.py` hides.
- **Example:** `secrets/api_key.py` defines `DEFAULT_KEY_PATH` and `DEFAULT_SUBPROC_COMMAND`, but `secrets/__init__.py` only exports `get_key` via `from .api_key import get_key`. So a developer doing `import brute.secrets as api` knows the constants are "off limits" while `get_key()` is fair game.
- **Entry point:** When brute starts, the top-level `__init__.py` imports `model_client as client` and `model_tools as tools`.

In short: it treats the `__init__.py` hierarchy as a filter separating a module's public interface from its internals.

You> quit
```
