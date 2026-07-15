# Code Audit Report — V2

**Date:** 2026-07-15  
**Project:** e-commerce-api-python  
**Branch:** develop  
**Previous audit:** [code-audit-v1.md](code-audit-v1.md) (30 findings)

---

## Progress since V1

| Status | Count |
|--------|-------|
| ✅ Fixed | 16 |
| 🔄 Partial | 1 |
| ❌ Remaining | 13 |
| **Total original** | **30** |

### Fixed in V1 → V2

| # | Issue |
|---|-------|
| 1 | `UserRepositoryImpl` — `await` on synchronous `delete()` |
| 2 | `BaseEntity.mark_as_updated()` writes wrong attribute |
| 3 | `UserRepository` abstract methods not `async` |
| 4 | `UserRepository.save()` returns DTO instead of entity |
| 5 | `UserModelMapper.to_user_entity()` — no null guard |
| 6 | `UserModelMapper.to_user_model()` — missing fields |
| 7 | `UpdateUserUseCase` — direct assignment to read-only properties |
| 8 | Config YAML typo `max_over_flow` |
| 9 | Duplicate `BaseModel` dead code deleted |
| 10 | Duplicate `PostgresDbConnection` dead code deleted |
| 11 | `UserEntity.password` made private with `@property` |
| 13 | `GetUserByIdUseCase` passes raw `UUID` instead of `EntityId` |
| 15 | Create route catches bare `Exception` (added `IntegrityError` / `OperationalError`) |
| 16 | `AppConfig` retries restricted to `IOError`/`OSError` |
| 18 | `DateTime(timezone=True)` standardised in `BaseModel` |
| 22 | Unused `UserEntity` import in `DeleteUserUseCase` |

---

## Remaining Findings

### Summary

| Severity | Count |
|----------|-------|
| Medium | 7 |
| Low | 6 |
| **Total** | **13** |

---

## Medium

### 12. `UserUpdateRequest` — cannot update password or role
- **File:** `src/app/features/user/application/dtos/user_dto.py` lines 29–34
- **Category:** Design
- **Description:** Only exposes `email`, `first_name`, `last_name`. No path for a caller to update their password or role via PATCH.
- **Fix:** Add `password: Optional[str] = None` and `role: Optional[str] = None`, or explicitly document these require separate endpoints.

### 14. Composition — injects concrete `UserRepositoryImpl` instead of interface
- **File:** `src/app/composition/features/users.py` lines 20–34
- **Category:** Architecture
- **Description:** All use-case factories depend on `UserRepositoryImpl` (concrete) instead of `UserRepository` (interface). Violates Dependency Inversion Principle; makes unit testing harder without a real database.
- **Fix:** Change type hints and `Depends` arguments to use `UserRepository`.

### 17. `requirements.txt` vs `pyproject.toml` — duplicate and conflicting dependencies _(partial)_
- **Files:** `requirements.txt`, `Dockerfile`, `pyproject.toml`
- **Category:** Consistency
- **Description:** `pyproject.toml` now has all production dependencies (including `aiosqlite` and `python-json-logger` added in V2). However, `requirements.txt` still lists raw packages including dev deps (`pytest`, duplicate `pyaml_env~=1.2.2`), and `Dockerfile` still installs from `requirements.txt` instead of `pyproject.toml`.
- **Fix:** Replace `requirements.txt` content with a lock-file stub and update `Dockerfile` to use `pip install .`.

### 19. `to_user_response()` — misleading `Union[BaseModel, UserEntity]` type hint
- **File:** `src/app/features/user/application/mappers/user_mapper.py` line 14
- **Category:** Design
- **Description:** Typed as `Union[BaseModel, UserEntity]` but only works correctly with `UserEntity`. Accessing `.email.value` would fail on a plain Pydantic model.
- **Fix:** Change to `def to_user_response(user_entity: UserEntity) -> UserResponse:`.

### 20 & 29. Migration — redundant non-unique index contradicts `UniqueConstraint` on email
- **File:** `alembic/versions/43a57a0d9e2c_initial_schema.py` lines 28–33
- **Category:** Consistency
- **Description:** Creates `UniqueConstraint("email")` and a separate `unique=False` index on the same column. The constraint already implies a unique index in PostgreSQL. The `unique=False` is also semantically contradictory.
- **Fix:** Remove the `create_index` call from the migration. A follow-up migration is needed to drop `ix_users_email` from running databases.

### 21. `UserModel.password` column too short for all bcrypt variants
- **File:** `src/app/features/user/infrastructure/models/user_model.py` line 16
- **Category:** Consistency
- **Description:** Column is `String(60)` but bcrypt can produce hashes up to 72 bytes. A future bcrypt version producing longer hashes would be silently truncated.
- **Fix:** Change to `String(72)` to match the bcrypt max output size. Requires a new Alembic migration to `ALTER COLUMN`.

---

## Low

### 23. User routes — unused use-case class imports
- **File:** `src/app/features/user/presentation/user_routes.py` lines 6–9
- **Category:** Dead code
- **Description:** `CreateUserUseCase`, `DeleteUserUseCase`, `GetUserByIdUseCase`, `UpdateUserUseCase` are imported but never referenced directly — they are injected via `Depends`.
- **Fix:** Remove lines 6–9.

### 24. Composition functions are `async` but never `await`
- **File:** `src/app/composition/features/users.py` lines 15–34
- **Category:** Design
- **Description:** All dependency provider factories are `async def` with no `await` inside. Unnecessary coroutine overhead.
- **Fix:** Remove `async` from all four factory functions.

### 25. `AppConfig` singleton — error message references wrong class name
- **File:** `src/app/config/app_config.py` lines 26–28
- **Category:** Design
- **Description:** `RuntimeError` raised in `__init__` references the wrong class name.
- **Fix:** Update the `RuntimeError` message to correctly reference `AppConfig.instance()`.

### 26. `BaseEntity` — no distinction between "create new" vs "reconstitute from DB"
- **File:** `src/app/shared/domain/entities/base_entity.py` lines 16–17
- **Category:** Design
- **Description:** Defaulting `created_at`/`updated_at` to `now()` silently overwrites stored timestamps when reconstructing from DB if callers forget to pass them.
- **Fix:** Consider a separate `reconstitute()` factory method vs `create()` to make intent explicit.

### 27. `config_util.py` — docstring parameter order is reversed
- **File:** `src/app/shared/utils/config_util.py` lines 3–8
- **Category:** Consistency
- **Description:** `:param key:` describes "The value" and `:param config:` describes "The key" — swapped vs the actual function signature.
- **Fix:** Reorder docstring params to match the signature: `config`, `key`, `default`, `expected_type`.

### 28. `alembic/env.py` — stale commented scaffold lines
- **File:** `alembic/env.py` lines 31–32
- **Category:** Dead code
- **Fix:** Remove the leftover Alembic template comments.

### 30. `UserResponse.id` typed as `str` instead of `UUID`
- **File:** `src/app/features/user/application/dtos/user_dto.py`
- **Category:** Consistency
- **Description:** Response DTO returns `id: str` rather than `UUID`. Weakly typed; clients cannot distinguish valid UUIDs from arbitrary strings at the contract level.
- **Fix:** Change to `id: UUID` with Pydantic serialisation.
