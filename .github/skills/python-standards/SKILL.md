---
name: python-standards
description: Audits Python code for language standards — PEP 8 style, type hints (PEP 484/604), naming, idiomatic patterns, project structure, dependencies, error handling, logging, testing, security.
version: 1.0.0
tags: [audit, python, pep8, type-hints, best-practices, backend]
---

# Python Standards Skill

Inspects Python backend for violations of **Python language standards and best practices** — expectations for production-quality code.

Covers: Style (PEP 8), Naming, Type Annotations, Idiomatic Python, Project Structure, Error Handling, Logging, Testing, Security.

Each finding specifies: standards area, file path, severity, evidence, remediation.

---

## Standards Areas

---

### 1 — PEP 8: Style and Formatting

> *"Code is read much more often than it is written."*

**Look for:**
- Wrong indentation (not 4 spaces — tabs, 2-space)
- Lines exceeding configured limit (flag if no config and regularly >120 chars)
- Import ordering wrong (not: stdlib, third-party, local with blank lines between)
- Wildcard imports (`from module import *`)
- Unused imports
- Whitespace issues (missing around operators, before colons, inconsistent blank lines)
- No formatter configured (`black`, `ruff format`, `autopep8` in config/pre-commit)

**Severity:**
- Wildcard imports in production: **High**
- No formatter, widespread inconsistent style: **Medium**
- Unused imports across multiple files: **Medium**
- Inconsistent indentation (mixed tabs/spaces): **Medium**
- Minor whitespace issues: **Low**
- Lines slightly over limit: **Low**

**Evidence:** File path, line #, PEP 8 rule violated, formatter configured?, snippet

---

### 2 — Naming Conventions

> *"There are only two hard things: cache invalidation and naming things."*

**Look for:**
- Classes not `PascalCase` (`class user_service`, `class userService`)
- Functions/methods not `snake_case` (`def getUserById`, `def GetUser`)
- Variables/attributes not `snake_case` (`userName`, `orderTotal`)
- Constants not `UPPER_SNAKE_CASE` (module-level `max_retries = 3`)
- Modules not lowercase `snake_case` (`UserService.py`, `orderProcessing.py`)
- Misuse of `_private`, `__dunder__`
- Booleans without predicates (`active` vs. `is_active`)
- Cryptic abbreviations in domain logic (`usr`, `mgr`, `proc`, `cfg`)
- Single-letter names outside comprehensions/formulas

**Severity:**
- Classes using `snake_case`/`camelCase` project-wide: **High**
- `camelCase` functions/variables widely used: **High**
- Module files in `PascalCase`/`camelCase`: **Medium**
- Single-letter variable outside comprehension: **Low**
- One-off naming inconsistency: **Low**

**Evidence:** File path, line #, offending name, expected convention, pattern across codebase?

---

### 3 — Type Annotations

> *"Type hints improve clarity, enable IDE support, and catch bugs before runtime."*

**Look for:**
- Missing return type annotations (especially public methods/API functions)
- Missing parameter type annotations (public/exported functions)
- Excessive `Any` usage (>10% of annotated functions)
- Old-style hints (`typing.Optional[X]` vs. `X | None` on Python 3.10+, `typing.List` vs. `list`)
- Missing `-> None` on void functions
- `# type: ignore` comments everywhere (types wrong, being silenced)
- No type checker configured (`mypy`, `pyright`, `pytype`, `basedpyright` in dev deps/CI)
- Strings instead of Enums/Literals for type safety

**Severity:**
- No type annotations anywhere: **High**
- Public API functions missing annotations: **High**
- Excessive `Any` (>10%): **Medium**
- No type checker in dev deps/CI: **Medium**
- Old-style `typing.Optional`/`List` on Python 3.10+: **Low**
- Missing `-> None`: **Low**
- Few `# type: ignore` comments (<5): **Low**

**Evidence:** File path, function signature, missing annotations, project Python version, type checker configured?

---

### 4 — Idiomatic Python (Pythonic Code)

> *"There should be one obvious way to do it."* — Zen of Python

**Look for:**
- Manual index iteration (`for i in range(len(items))` vs. `for item in items` or `enumerate`)
- Manual dict key-checking (`if key in d: value = d[key]` vs. `d.get(key)`)
- Not using comprehensions (building list with loop + `.append()`)
- Not using context managers (manual `open()`/`close()`, `acquire()`/`release()`)
- String concatenation in loops (`+=` vs. `"".join()` or f-strings)
- Mutable default arguments (`def func(items=[])`)
- Using `==` with `None`/`True`/`False` (should use `is None`, `is True`, `is False`)
- Bare `except:` (catches `KeyboardInterrupt`, `SystemExit`)
- Not using `pathlib` (string manipulation for paths)
- Reimplementing stdlib (`itertools`, `collections`, `functools`, `dataclasses`)
- Using `type()` instead of `isinstance()`
- Using dicts/tuples instead of dataclasses/Pydantic
- Global mutable state without thread safety

**Severity:**
- Mutable default arguments used across codebase: **High**
- Bare `except:`: **High**
- Global mutable state without thread safety: **High**
- Manual file/resource management without context managers: **Medium**
- Widespread `for i in range(len(...))`: **Medium**
- Not using `pathlib`: **Low**
- Not using comprehensions where cleaner: **Low**

**Evidence:** File path, line #, non-idiomatic pattern, idiomatic alternative

---

### 5 — Project Structure and Packaging

> *"A well-structured project is easier to navigate, test, and deploy."*

**Look for:**
- No `pyproject.toml` (relying only on `setup.py`/`setup.cfg` without PEP 517/518/621)
- No clear source layout (all files in repo root vs. `src/` or package directory)
- Missing `__init__.py` in packages (non-namespace packages)
- Circular imports (modules import each other → `ImportError` or import-inside-function workarounds)
- No `.gitignore` for Python (`__pycache__`, `*.pyc`, `.mypy_cache`, `.pytest_cache`, `dist/`, `*.egg-info`)
- Secrets/credentials in source (`.env` files, API keys, passwords committed)
- No dependency pinning (`requests` vs. `requests>=2.28,<3` or no lock file)
- `requirements.txt` only (no `pyproject.toml [project.dependencies]` for installable lib/app)
- Monolithic modules (single files >500-1000 lines with unrelated classes/functions)

**Severity:**
- Secrets/API keys/passwords committed: **Critical**
- Circular imports causing runtime errors: **High**
- No clear package structure (all files in root): **High**
- No `pyproject.toml` and no `setup.py`/`setup.cfg`: **Medium**
- No `.gitignore` for Python: **Medium**
- Unpinned dependencies, no lock file: **Medium**
- Monolithic 1000+ line modules: **Medium**
- Missing `__init__.py`: **Low**

**Evidence:** Folder structure, missing/misconfigured files, circular import chain, secrets found (redacted values)

---

### 6 — Error Handling

> *"Errors should never pass silently."* — Zen of Python

**Look for:**
- Bare `except:` (catches `SystemExit`, `KeyboardInterrupt`, `GeneratorExit`)
- Broad `except Exception:` without discrimination (only acceptable at top-level with logging)
- Silent swallowing (`except Exception: pass`)
- String exceptions or bare `raise` outside except
- Missing exception context (`raise NewException()` vs. `raise NewException() from original`)
- Returning error codes (`None`, `-1`, `{"error": ...}`) instead of raising
- Overly granular try/except (wrapping every line instead of letting propagation)
- No custom exception hierarchy (all `Exception`, `ValueError`, `RuntimeError`)
- Missing finally/cleanup (resources not using try/finally or context managers)
- Catching and re-raising without adding context (`except Exception as e: raise e`)

**Severity:**
- `except: pass` or `except Exception: pass` hiding errors in critical paths: **Critical**
- Bare `except:` in production: **High**
- Missing exception chain across codebase: **Medium**
- No custom exception classes: **Medium**
- Returning error codes in internal APIs: **Medium**
- Broad `except Exception:` with proper logging: **Low**
- Missing `from` in single isolated raise: **Low**

**Evidence:** File path, line #, try/except block, exception types caught, handler action, impact

---

### 7 — Logging

> *"Print statements are not a logging strategy."*

**Look for:**
- `print()` for operational output (not CLI tools/scripts)
- No logging configuration (imported but never configured)
- Logging secrets/PII (passwords, tokens, API keys, credit cards, emails)
- Wrong log levels (`logger.info()` for errors, `logger.error()` for info messages)
- No structured logging (plain strings vs. key-value pairs in production services — recommendation not hard rule)
- String formatting in log calls (`logger.info(f"Got {value}")` vs. `logger.info("Got %s", value)`)
- Missing exception info (`logger.error(f"Failed: {e}")` vs. `logger.exception("Failed")` or `exc_info=True`)
- No log correlation (no request ID/correlation ID in multi-user services)

**Severity:**
- Logging secrets/tokens/PII: **Critical**
- `print()` throughout production as primary output: **High**
- No logging configuration in service/application: **High**
- Missing `exc_info`/`logger.exception()` across codebase: **Medium**
- Wrong log levels systematically: **Medium**
- f-string in log calls (performance): **Low**
- No structured logging in smaller project: **Low**

**Evidence:** File path, line #, `print()`/`logger.*()` call, info logged (flag if sensitive), logging configured?

---

### 8 — Testing Conventions

> *"Code without tests is broken by design."*

**Look for:**
- No tests at all (no `tests/` dir, no `pytest`/`unittest` in deps)
- No test runner configured (not in dev deps or `pyproject.toml [tool.pytest]`)
- Tests with no assertions (pass regardless of correctness)
- Tests depend on external services without mocking (require live DB/API/network)
- No test isolation (shared mutable state, fail in different order)
- No fixtures/factories (every test manually constructs complex data)
- Test files not following naming (`test_*.py` or `*_test.py` — may not be discovered)
- No coverage configuration (no `pytest-cov`, `coverage.py`)
- Tests mixed with source code (in source package vs. separate `tests/` dir)

**Severity:**
- No tests in production project: **Critical**
- Tests assert nothing (false coverage): **High**
- Tests require live external services, no mock/fake: **High**
- No test runner in dependencies: **High**
- Tests share mutable state, break in parallel: **Medium**
- No coverage configuration: **Medium**
- Test files not following naming: **Medium**
- Tests mixed with source: **Low**
- Missing fixtures for complex setup: **Low**

**Evidence:** `tests/` dir exists?, test runner/coverage in deps, files with no assertions, tests making external calls

---

### 9 — Security Hygiene

> *"Security is a process, not a product."*

**Look for:**
- Hardcoded secrets (API keys, passwords, tokens, connection strings)
- `eval()`/`exec()` with user input (arbitrary code execution)
- `pickle` with untrusted data (`pickle.loads()` on external data)
- `subprocess` with `shell=True` and user input (command injection)
- SQL injection (string formatting in queries vs. parameterized)
- `yaml.load()` without `Loader=SafeLoader`
- Debug mode in production config (`DEBUG = True`, `app.run(debug=True)`)
- Overly permissive CORS (`allow_origins=["*"]` in production)
- No dependency vulnerability scanning (`safety`, `pip-audit`, `snyk`, `dependabot`)
- Insecure random (`random` vs. `secrets` for tokens/passwords/session IDs)
- `assert` for validation (stripped with `-O` flag)

**Severity:**
- Hardcoded secrets: **Critical**
- `eval()`/`exec()` with user input: **Critical**
- `pickle.loads()` on external/untrusted data: **Critical**
- SQL injection via string formatting: **Critical**
- `subprocess` with `shell=True` + user input: **Critical**
- `yaml.load()` without safe loader: **High**
- Debug mode in production config: **High**
- `assert` for input validation/security: **High**
- `random` instead of `secrets` for security values: **High**
- Overly permissive CORS in production: **Medium**
- No dependency vulnerability scanning: **Medium**
- Insecure default settings overridden in production: **Low**

**Evidence:** File path, line #, vulnerable code (redact secret values), attack vector, suggested fix

---

## Audit Instructions

1. **Determine Python version and tooling** — check `pyproject.toml`, `setup.cfg`, `.python-version`, etc. for target version. Check for linters (`ruff`, `flake8`), formatters (`black`), type checkers (`mypy`, `pyright`), test runners (`pytest`).
2. **Traverse source tree** — `.py` files in source directories. Skip venvs (`venv/`, `.venv/`), auto-generated, migrations, vendored code.
3. **For each area (1-9)**, review files using "Look for" patterns.
4. **Collect findings** with: standards area, file path, line #, title, snippet, severity, remediation.
5. **Report only observable violations** — backed by code patterns.
6. **Respect project's configured standards** — defer to project's explicit config (line length, etc.) over default PEP 8.
7. **Classify conservatively** — when in doubt, choose lower severity.
