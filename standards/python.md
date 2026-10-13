# Python Engineering Standards

These standards establish the baseline for high-performance, strictly typed, and maintainable Python services.

---

## 1. Tooling & Environment

- **Package Manager:** `uv` exclusively. No pip, poetry, or pipenv.
- **Python Version:** Pin `requires-python = "==3.13.5"` in `pyproject.toml` and `.python-version`.
- **Dependency Pinning:**
  - Strict immutable version pinning (e.g. `pydantic = "2.10.6"`, never `pydantic = "^2.10.6"`).
  - Dependencies must be sorted **alphabetically** in `pyproject.toml`.
  - Virtual environments (`.venv`) are strictly local and ignored in version control and Docker builds.

---

## 2. Code Quality & Formatting (Ruff & Mypy)

- **Ruff:** Official unified linter, import sorter, and formatter.
  ```powershell
  # Check and auto-fix modern idioms and imports
  uvx ruff check . --exclude .venv --fix

  # Format according to style guide
  uvx ruff format . --exclude .venv
  ```
- **Mypy:** Static typing verification across all modules and schemas.
  ```powershell
  uvx mypy . --ignore-missing-imports --exclude .venv
  ```

---

## 3. Strict Typing & Modern Idioms (PEP 585 & PEP 604)

- **Native Collections:**
  - Always use `list[str]`, `dict[str, Any]`, `set[int]`, `tuple[str, ...]`.
  - Avoid legacy `typing.List`, `typing.Dict`, `typing.Set`, `typing.Tuple`.
- **Union Syntax:**
  - Always use `str | None` instead of `Optional[str]`.
  - Always use `int | float` instead of `Union[int, float]`.
- **Closed-Set Discrete Values:**
  - Never use raw `str` for discrete fields (e.g. `status`, `stage`, `action`).
  - Use `Literal["pending", "running", "completed"]` or `enum.StrEnum`.
  - Guarantees compile-time verification in Mypy and deterministic OpenAPI/JSON schemas for LLMs.
- **Hermetic Tool & API Schemas:**
  - Avoid `Any` in public boundaries.
  - Every tool input and output must be modeled with a Pydantic model featuring `Field(description=...)`.
  - Mutable defaults MUST use callable factories:
    ```python
    from pydantic import BaseModel, Field

    class TaskConfig(BaseModel):
        # CORRECT:
        tags: list[str] = Field(default_factory=list)
        metadata: dict[str, str] = Field(default_factory=dict)

        # INCORRECT (causes state leakage in concurrent async workers):
        # tags: list[str] = Field(default=[])
    ```

---

## 4. Path & File Operations

- Always use `pathlib.Path` for cross-platform filesystem handling:
  ```python
  from pathlib import Path

  base_dir = Path(__file__).resolve().parent
  config_file = base_dir / "config.json"
  ```
- Never use legacy `os.path.join`, `os.path.exists`, or hardcoded Windows backslashes (`\`).
