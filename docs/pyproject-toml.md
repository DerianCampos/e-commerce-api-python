# pyproject.toml — Dependency & Project Management

`pyproject.toml` is the **single source of truth** for all project metadata and dependencies in this repository. `requirements.txt` is a generated artifact only — do not edit it manually.

---

## Why pyproject.toml?

| Old way | New way |
|---|---|
| `requirements.txt` (production) | `pyproject.toml → [project.dependencies]` |
| `requirements-dev.txt` (dev tools) | `pyproject.toml → [project.optional-dependencies.dev]` |
| `setup.cfg` / `setup.py` (metadata) | `pyproject.toml → [project]` |
| Scattered tool configs | `pyproject.toml → [tool.*]` |

A single file replaces all of the above, following [PEP 517](https://peps.python.org/pep-0517/), [PEP 518](https://peps.python.org/pep-0518/), and [PEP 621](https://peps.python.org/pep-0621/).

---

## File Structure

```toml
[build-system]          # How the package is built (setuptools, hatch, etc.)
[project]               # Package metadata + production dependencies
[project.optional-dependencies]  # Dev / test / docs extras
[tool.pytest.ini_options]        # pytest config
[tool.mypy]                      # mypy type-checker config
[tool.ruff]                      # Ruff linter + formatter config
```

### `[build-system]`

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"
```

Declares which build backend pip should use. Required for `pip install .` to work.

---

### `[project]`

```toml
[project]
name = "e-commerce-api"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi==0.115.11",
    ...
]
```

- `name` — package name used by pip and PyPI.
- `version` — follows [SemVer](https://semver.org/).
- `requires-python` — minimum Python version; pip enforces this.
- `dependencies` — **production-only** packages. These are installed in Docker.

---

### `[project.optional-dependencies]`

```toml
[project.optional-dependencies]
dev = [
    "pytest==7.4.2",
    "pytest-asyncio>=0.21.0",
    "httpx>=0.24.1",
    "mypy>=1.5.0",
    "ruff>=0.1.0",
]
```

Groups of extras installed on demand. Dev tools are **never** installed in the Docker production image.

---

### `[tool.pytest.ini_options]`

Replaces `pytest.ini` or `setup.cfg [tool:pytest]`. Controls how pytest discovers and runs tests.

---

### `[tool.mypy]` and `[tool.ruff]`

Static analysis and linting configuration embedded directly in the project file instead of separate `.mypy.ini` / `.ruff.toml` files.

---

## Common Commands

### Install production dependencies (Docker / CI)

```bash
pip install .
```

### Install dev dependencies locally

```bash
pip install ".[dev]"
```

### Install in editable mode (recommended for local development)

```bash
pip install -e ".[dev]"
```

Changes to `src/` are reflected immediately without reinstalling.

### Regenerate requirements.txt lock file (pin exact versions)

Requires [pip-tools](https://pip-tools.readthedocs.io/):

```bash
pip install pip-tools
pip-compile pyproject.toml --output-file requirements.txt
```

Run this whenever you add or upgrade a dependency in `pyproject.toml`.

### Check for outdated dependencies

```bash
pip list --outdated
```

### Run linter (ruff)

```bash
ruff check src/
ruff format src/
```

### Run type checker (mypy)

```bash
mypy src/
```

### Run tests

```bash
pytest
# or with coverage:
pytest --cov=src
```

---

## Adding a Dependency

1. Add the package to `[project.dependencies]` in `pyproject.toml` (production) or `[project.optional-dependencies.dev]` (dev tooling).
2. Re-run `pip install -e ".[dev]"` locally.
3. Regenerate `requirements.txt` with `pip-compile`.
4. Commit both `pyproject.toml` and `requirements.txt`.

**Never add packages directly to `requirements.txt` — they will be overwritten on the next compile.**

---

## Docker Behaviour

The `Dockerfile` installs production deps via:

```dockerfile
COPY pyproject.toml .
RUN pip install --no-cache-dir .
```

Only `[project.dependencies]` are installed — dev extras (`[dev]`) are excluded automatically.
