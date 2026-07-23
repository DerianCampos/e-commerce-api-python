# Code Audit Report

**Date:** 2026-07-14  
**Project:** e-commerce-api-python  
**Branch:** develop  

---

## Summary

| Severity | Count |
|----------|-------|
| Critical | 1 |
| High | 9 |
| Medium | 11 |
| Low | 9 |
| **Total** | **30** |

---

## Critical

### 1. `UserRepositoryImpl` — `await` on synchronous `delete()`
- **File:** `src/app/features/user/infrastructure/repository/user_repository_impl.py` line 143
- **Category:** Bug
- **Description:** `await self.db_session.delete(existing)` — SQLAlchemy's `session.delete()` is synchronous. Using `await` raises `TypeError` at runtime when deleting a user.
- **Fix:** Remove `await` → `self.db_session.delete(existing)`

---

## High

### 2. `BaseEntity.mark_as_updated()` writes wrong attribute
- **File:** `src/app/shared/domain/entities/base_entity.py` line 21
- **Category:** Bug
- **Description:** Sets `self._updated_at` (nonexistent private field) instead of `self.updated_at`. Every call to `mark_as_updated()` silently does nothing.
- **Fix:** Change to `self.updated_at = datetime.now()`

### 3. `UserRepository` abstract methods are not `async`
- **File:** `src/app/features/user/domain/repositories/user_repository.py` lines 7–20
- **Category:** Architecture
- **Description:** Interface defines synchronous `@abstractmethod` signatures while `UserRepositoryImpl` uses `async def`. Contract mismatch breaks type safety.
- **Fix:** Add `async` to all abstract method signatures in `UserRepository`.

### 4. `UserRepository.save()` returns `UserResponse` (DTO), not `UserEntity`
- **File:** `src/app/features/user/domain/repositories/user_repository.py` line 13
- **Category:** Design
- **Description:** `save()` is typed to return `UserResponse` (application-layer DTO) while `update()` returns `Optional[UserEntity]`. Domain repositories must not return DTOs.
- **Fix:** Change return type of `save()` to `UserEntity`.

### 5. `UserModelMapper.to_user_entity()` — no null guard
- **File:** `src/app/features/user/infrastructure/mappers/user_model_mapper.py` lines 17–30
- **Category:** Bug
- **Description:** If `user_model` is `None` (record not found), accessing `user_model.id` raises `AttributeError` on every failed lookup.
- **Fix:** Add at top of method: `if user_model is None: return None`

### 6. `UserModelMapper.to_user_model()` — missing fields
- **File:** `src/app/features/user/infrastructure/mappers/user_model_mapper.py` lines 8–15
- **Category:** Bug
- **Description:** Only maps `id`, `email`, `first_name`, `last_name`. Missing: `password`, `role`, `is_active`, `created_at`, `updated_at`.
- **Fix:** Add the missing field mappings to the returned dict.

### 7. `UpdateUserUseCase` — direct assignment to read-only properties
- **File:** `src/app/features/user/application/use_cases/update_user.py` lines 35–41
- **Category:** Design
- **Description:** Directly assigns to `@property` accessors backed by private fields, bypassing `update()` and `mark_as_updated()`.
- **Fix:** Replace direct assignments with `existing_user.update(email=..., first_name=..., last_name=...)`

### 8. Config YAML — typo `max_over_flow` instead of `max_overflow`
- **Files:** All config YAMLs (`config_local.yml`, `config_dev.yml`, `config_test.yml`, `config_stage.yml`, `config_prod.yml`, `config_container.yml`) line ~15
- **Category:** Bug
- **Description:** All YAMLs use `max_over_flow` but `engine_factory.py` reads `max_overflow`. The pool setting is silently ignored and the engine runs with the SQLAlchemy default.
- **Fix:** Rename key to `max_overflow` in all config files.

### 9. Duplicate `BaseModel` class — dead code
- **Files:** `src/app/shared/persistence/base_model.py` and `src/app/shared/infrastructure/postgres/models/base_model.py`
- **Category:** Dead code
- **Description:** The `/infrastructure/postgres/models/` version is never imported anywhere. Creates confusion about the canonical source.
- **Fix:** Delete `src/app/shared/infrastructure/postgres/models/base_model.py`.

### 10. Duplicate `PostgresDbConnection` — dead code
- **Files:** `src/app/shared/persistence/postgres.py` and `src/app/shared/infrastructure/postgres/config/postgres_db_conn.py`
- **Category:** Dead code
- **Description:** Two PostgreSQL connection implementations with differing config key conventions. Only the `persistence/` version is used.
- **Fix:** Delete `src/app/shared/infrastructure/postgres/config/postgres_db_conn.py`.

---

## Medium

### 11. `UserEntity` — `password` is public; all other fields are private
- **File:** `src/app/features/user/domain/entities/user_entity.py` line 24
- **Category:** Design
- **Description:** `self.password = password` is public while all other fields use private `_` prefix with `@property`. Inconsistent encapsulation allows direct mutation of the password from outside the entity.
- **Fix:** Rename to `self._password = password` and expose via `@property def password(self) -> HashedPassword`.

### 12. `UserUpdateRequest` — cannot update password or role
- **File:** `src/app/features/user/application/dtos/user_dto.py` lines 29–34
- **Category:** Design
- **Description:** Only exposes `email`, `first_name`, `last_name`. No path for a caller to update their password or role via PATCH.
- **Fix:** Add `password: Optional[str] = None` and `role: Optional[str] = None`, or explicitly document these require separate endpoints.

### 13. `GetUserByIdUseCase` — passes raw `UUID` instead of `EntityId`
- **File:** `src/app/features/user/application/use_cases/get_user_by_id.py` lines 18–21
- **Category:** Design
- **Description:** Creates `user_obj_id = EntityId(user_uuid)` but then passes raw `user_uuid` to `find_by_id()` instead of `user_obj_id`.
- **Fix:** Change to `await self.user_repository.find_by_id(user_obj_id)`.

### 14. Composition — injects concrete `UserRepositoryImpl` instead of interface
- **File:** `src/app/composition/features/users.py` lines 20–34
- **Category:** Architecture
- **Description:** All use-case factories depend on `UserRepositoryImpl` (concrete) instead of `UserRepository` (interface). Violates Dependency Inversion Principle; makes unit testing harder without a real database.
- **Fix:** Change type hints and `Depends` arguments to use `UserRepository`.

### 15. Create route — catches bare `Exception`, returns 500 for all errors
- **File:** `src/app/features/user/presentation/user_routes.py` line 38
- **Category:** Design
- **Description:** A duplicate email (`IntegrityError`) returns HTTP 500 instead of 409 Conflict. All database errors are indistinguishable from application bugs from the client's perspective.
- **Fix:** Add `except IntegrityError` → 409, `except OperationalError` → 503 before the generic catch.

### 16. `AppConfig` — retries on all exceptions including deterministic config errors
- **File:** `src/app/config/app_config.py` lines 69–97
- **Category:** Design
- **Description:** `@retry_on_exception()` retries `FileNotFoundError` and `ValueError` from config loading. Config errors are deterministic; retrying masks bugs and delays startup.
- **Fix:** Restrict retry to transient I/O errors only (`IOError`, `OSError`).

### 17. `requirements.txt` vs `pyproject.toml` — duplicate and conflicting dependencies
- **Files:** `requirements.txt`, `pyproject.toml`
- **Category:** Consistency
- **Description:** Dependencies declared in both files with version specifier inconsistencies (`pyaml_env~=1.2.2` vs `pyaml-env==1.2.2`). Dev deps (`pytest`) mixed into `requirements.txt` production list.
- **Fix:** Use `pyproject.toml` as single source of truth; keep `requirements.txt` as a generated lock file only.

### 18. `DateTime` timezone inconsistency between models
- **Files:** `src/app/shared/infrastructure/postgres/models/base_model.py` vs `src/app/features/user/infrastructure/models/user_model.py`
- **Category:** Consistency
- **Description:** Infrastructure `BaseModel` uses `DateTime` without timezone; `UserModel` uses `DateTime(timezone=True)`. Timestamp comparisons will break if both are in use.
- **Fix:** Standardise on `DateTime(timezone=True)` everywhere.

### 19. `to_user_response()` — misleading `Union[BaseModel, UserEntity]` type hint
- **File:** `src/app/features/user/application/mappers/user_mapper.py` line 14
- **Category:** Design
- **Description:** Typed as `Union[BaseModel, UserEntity]` but only works correctly with `UserEntity`. Accessing `.email.value` would fail on a plain Pydantic model.
- **Fix:** Change to `def to_user_response(user_entity: UserEntity) -> UserResponse:`.

### 20. Migration — redundant non-unique index alongside `UniqueConstraint` on email
- **File:** `alembic/versions/43a57a0d9e2c_initial_schema.py` lines 28–33
- **Category:** Consistency
- **Description:** Creates `UniqueConstraint("email")` and a separate `unique=False` index on the same column. The constraint already implies a unique index in PostgreSQL.
- **Fix:** Remove the `create_index` call, or change to `unique=True`.

### 21. `UserModel.password` column too short for all bcrypt variants
- **File:** `src/app/features/user/infrastructure/models/user_model.py` line 16
- **Category:** Consistency
- **Description:** Column is `String(60)` but bcrypt can produce hashes up to 72 bytes. A future bcrypt version producing longer hashes would be silently truncated.
- **Fix:** Change to `String(72)` to match the bcrypt max output size.

---

## Low

### 22. `DeleteUserUseCase` — unused `UserEntity` import
- **File:** `src/app/features/user/application/use_cases/delete_user.py` line 5
- **Category:** Dead code
- **Fix:** Remove `from src.app.features.user.domain.entities.user_entity import UserEntity`.

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

### 29. Migration unique index `unique=False` contradicts constraint
- **File:** `alembic/versions/43a57a0d9e2c_initial_schema.py` line 33
- **Category:** Consistency
- **Description:** Index created with `unique=False` on the same column as a `UniqueConstraint`. Semantically contradictory.
- **Fix:** Set `unique=True` or remove the index entirely.

### 30. `UserResponse.id` typed as `str` instead of `UUID`
- **File:** `src/app/features/user/application/dtos/user_dto.py`
- **Category:** Consistency
- **Description:** Response DTO returns `id: str` rather than `UUID`. Weakly typed; clients cannot distinguish valid UUIDs from arbitrary strings at the contract level.
- **Fix:** Consider `id: UUID` with Pydantic serialisation, or document the expected UUID format.
