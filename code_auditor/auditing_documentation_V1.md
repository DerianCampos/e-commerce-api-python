# Backend Audit Report — V1
> Generated: April 16, 2026 (Updated: April 26, 2026 with DDD skill)  
> Skills applied: clean-architecture, dry-kiss-yagni, python-standards, solid-principles, domain-driven-design  
> Previous version: none

---

## Summary Table

| Severity  | Count |
|-----------|-------|
| Critical  | 4     |
| High      | 7     |
| Medium    | 9     |
| Low       | 7     |
| **Total** | **27** |

---

## Critical Issues

### [C-01] No test suite — production code completely untested
- **Location**: Project root (no `tests/` directory found)
- **File**: N/A (missing directory structure)
- **Link**: `tests/` ← **CREATE THIS DIRECTORY**
- **Skill**: python-standards
- **Description**: The project has zero tests. `pytest` is listed in `requirements.txt` but no test files exist (`test_*.py` or `tests/` directory). This is a critical gap — the entire application is running without any automated verification of correctness.
- **Evidence**: 
  - No `tests/` directory found in project structure
  - File search for `test_*.py` returned zero results
  - 69 Python files scanned, 0 test files
- **Impact**: Every code change risks introducing regressions with no safety net. Business logic in use cases, value object validation, repository implementations, and API endpoints are all unverified. This is unacceptable for production code.
- **Remediation**: Immediately establish a test suite:
  1. Create `tests/` directory with mirrors of `src/` structure
  2. Write unit tests for domain logic (value objects, entities)
  3. Write integration tests for repositories using test database
  4. Write API tests for endpoints using FastAPI `TestClient`
  5. Configure `pytest` in `pyproject.toml` and add to CI pipeline
  6. Target minimum 70% code coverage for critical paths

---

### [C-02] No `pyproject.toml` — project is not properly packaged
- **Location**: Project root
- **File**: `pyproject.toml` ← **MISSING FILE**
- **Link**: `/Users/deriancampos/GitHub/EndToEndLabCR/e-commerce-api-python/pyproject.toml` ← **CREATE THIS FILE**
- **Skill**: python-standards
- **Description**: The project uses only `requirements.txt` with no `pyproject.toml`, `setup.py`, or `setup.cfg`. This violates PEP 517/518/621 standards for modern Python packaging. The project cannot be installed as a package, has no metadata, and lacks tool configuration centralization.
- **Evidence**:
  - File search for `pyproject.toml` returned no results
  - File search for `setup.py` returned no results
  - Only `requirements.txt` exists for dependency management
- **Impact**: 
  - Cannot install the project as a package (`pip install -e .`)
  - No centralized configuration for tools (pytest, mypy, black, ruff)
  - Cannot publish to PyPI or private package registry
  - Dependencies are not properly pinned or locked
  - Dev dependencies mixed with production dependencies
- **Remediation**: Create `pyproject.toml` with:
  ```toml
  [build-system]
  requires = ["setuptools>=68.0", "wheel"]
  build-backend = "setuptools.build_meta"

  [project]
  name = "e-commerce-api"
  version = "0.1.0"
  requires-python = ">=3.10"
  dependencies = [
      "fastapi==0.115.11",
      # ... other runtime deps
  ]

  [project.optional-dependencies]
  dev = ["pytest>=7.4.2", "pytest-asyncio", "httpx", "mypy", "ruff"]

  [tool.pytest.ini_options]
  pythonpath = ["src"]
  asyncio_mode = "auto"

  [tool.ruff]
  line-length = 120
  target-version = "py310"
  ```

---

### [C-03] Broad exception catching with logging but continued execution risk
- **Location**: `src/app/features/user/infrastructure/postgres/repository/user_repository_impl.py`
- **Lines**: 75-85, 117-124, 133-140
- **Links**: 
  - [`user_repository_impl.py:75-85`](../src/app/features/user/infrastructure/postgres/repository/user_repository_impl.py#L75-L85)
  - [`user_repository_impl.py:117-124`](../src/app/features/user/infrastructure/postgres/repository/user_repository_impl.py#L117-L124)
  - [`user_repository_impl.py:133-140`](../src/app/features/user/infrastructure/postgres/repository/user_repository_impl.py#L133-L140)
- **Skill**: python-standards
- **Description**: Repository methods catch broad `Exception` in `try/except` blocks, log the error, and re-raise. However, in `save()` method, there's a pattern of catching `IntegrityError` separately then catching all other exceptions. The issue is that a bare `except Exception` can swallow critical issues including `KeyboardInterrupt` when not properly scoped.
- **Evidence**:
```python
# user_repository_impl.py, line 75-85
except IntegrityError as ie:
    await self.db_session.rollback()
    log.error(f"Integrity error saving user: {ie}")
    raise
except Exception as e:  # ← Catches too broadly
    await self.db_session.rollback()
    log.error(f"Unexpected error saving user: {e}")
    raise
```
- **Impact**: While the code does re-raise, catching `Exception` at the top level is a Python anti-pattern. It can catch system-level exceptions (`SystemExit`, `KeyboardInterrupt`) if not careful, though this code does re-raise so the impact is mitigated. The pattern still violates best practices.
- **Remediation**: Catch specific SQLAlchemy exceptions only:
```python
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError

except IntegrityError as ie:
    # ... handle integrity constraint violations
except (SQLAlchemyError, OperationalError) as e:
    # ... handle other database errors
```

---

### [C-04] Anemic Domain Model — UserEntity has no behavior, only data
- **Location**: `src/app/features/user/domain/entities/user_entity.py`
- **Lines**: 11-32 (entire class)
- **Link**: [`user_entity.py:11-32`](../src/app/features/user/domain/entities/user_entity.py#L11-L32)
- **Skill**: domain-driven-design (ADM — Anemic Domain Model)
- **Description**: `UserEntity` is a pure data structure with no domain behavior. All properties are public and directly mutable. There are no domain methods for operations like `change_email()`, `deactivate()`, `promote_to_admin()`, `change_password()`, or `update_profile()`. This forces all business logic into use cases and services, violating DDD's principle that **behavior belongs with data**.
- **Evidence**:
```python
class UserEntity(BaseEntity):
    def __init__(self, id: EntityId, email: Email, first_name: str, 
                 last_name: str, hashed_password: HashedPassword, 
                 role: Role, is_active: bool, ...):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.hashed_password = hashed_password
        self.role = role
        self.is_active = is_active
        # ... no methods beyond __init__
```
The entity has:
- ✅ 8 public data attributes
- ❌ 0 domain methods
- ❌ 0 invariant protection
- ❌ 0 business rule enforcement
- **Impact**: This is the textbook definition of an anemic domain model. Key consequences:
  - **Business logic scatters** across use cases (`SaveUser`, `DeleteUser`, etc.) instead of being cohesive in the entity
  - **Invariants cannot be enforced** — any code can set `is_active = False` or mutate `role` without validation
  - **No single source of truth** for "what can a User do?" — you have to read every use case to understand the domain
  - **Harder to test** — business rules are spread across multiple files instead of concentrated in testable domain methods
  - **Duplicate logic risk** — if two use cases both need to "deactivate a user," they'll likely repeat the logic
  - **Missing domain concepts** — operations like "promote to admin" or "change password" don't have a named domain method, they're just property assignments buried in use case code
- **Remediation**: Add domain methods to `UserEntity` that encapsulate business rules and protect invariants:
```python
class UserEntity(BaseEntity):
    # ...existing __init__...

    def change_email(self, new_email: Email) -> None:
        """Change user email. Domain rule: email must be unique (enforced by repo)."""
        if self.email == new_email:
            raise ValueError("New email is the same as current email")
        self.email = new_email
        self._mark_updated()

    def change_password(self, new_password: HashedPassword) -> None:
        """Change user password."""
        self.hashed_password = new_password
        self._mark_updated()

    def deactivate(self) -> None:
        """Deactivate user account. Business rule: cannot deactivate admin."""
        if self.role.is_admin:
            raise ValueError("Cannot deactivate admin users")
        self.is_active = False
        self._mark_updated()

    def activate(self) -> None:
        """Reactivate user account."""
        self.is_active = True
        self._mark_updated()

    def promote_to_admin(self) -> None:
        """Promote user to admin role."""
        if self.role.is_admin:
            raise ValueError("User is already an admin")
        self.role = Role.ADMIN
        self._mark_updated()

    def update_profile(self, first_name: str = None, last_name: str = None) -> None:
        """Update user profile information."""
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        self._mark_updated()

    def _mark_updated(self) -> None:
        """Internal helper to update timestamp."""
        from src.shared.utils.date_util import get_current_datetime
        self.updated_at = get_current_datetime()
```
Then refactor use cases to call these methods instead of direct property access:
```python
# Before (in use case):
user_entity.is_active = False
user_entity.updated_at = get_current_datetime()

# After (in use case):
user_entity.deactivate()
```

---

## High Priority Issues

### [H-01] UserService violates Single Responsibility Principle (SRP)
- **Location**: `src/app/features/user/application/services/user_service.py`
- **Lines**: 1-34 (entire file)
- **Link**: [`user_service.py`](../src/app/features/user/application/services/user_service.py)
- **Skill**: solid-principles (SRP)
- **Description**: The `UserService` class is a thin pass-through layer that instantiates use cases and immediately delegates to them. This violates SRP because the service layer adds no business value — it's purely orchestrating use case construction. The service exists but serves no purpose, creating unnecessary indirection.
- **Evidence**:
```python
class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_by_id(self, user_id: str):
        use_case = GetUserByIdUseCase(self.user_repository)
        return await use_case.execute(user_id)
    
    async def save_user(self, user_create: UserCreate) -> UserResponse:
        use_case = SaveUser(self.user_repository)
        return await use_case.execute(user_create)
    # ... same pattern for update and delete
```
Every method follows the same pattern: instantiate use case → call execute → return result. No validation, transformation, or business logic happens here.
- **Impact**: Adds cognitive load and maintenance overhead with no benefit. Developers must navigate through an extra layer to understand the code path. If business logic is later added to this service, it will compete with use case logic, creating confusion about where logic belongs.
- **Remediation**: Remove `UserService` entirely and inject use cases directly into route handlers via FastAPI dependencies. Alternatively, if the service layer is meant to compose multiple use cases or add cross-cutting concerns (transaction management, authorization checks, event publishing), implement that logic explicitly.

**Severity rationale**: Marking as High rather than Critical because the code functions correctly — it's a design issue that impacts maintainability but not runtime correctness.

---

### [H-02] Missing type annotations on return types across multiple use cases
- **Location**: `src/app/features/user/application/services/user_service.py`
- **Line**: 14
- **Link**: [`user_service.py:14`](../src/app/features/user/application/services/user_service.py#L14)
- **Skill**: python-standards
- **Description**: The `get_user_by_id` service method is missing an explicit return type annotation. While some methods have them (`save_user() -> UserResponse`), consistency is lacking.
- **Evidence**:
```python
async def get_user_by_id(self, user_id: str):  # ← Missing -> UserResponse
    use_case = GetUserByIdUseCase(self.user_repository)
    return await use_case.execute(user_id)
```
- **Impact**: Reduces type safety. IDEs cannot provide accurate type hints for callers. Mypy cannot verify return type compatibility.
- **Remediation**: Add explicit return type annotations to all public methods:
```python
async def get_user_by_id(self, user_id: str) -> UserResponse:
```

---

### [H-03] `UpdateUserUseCase` mutates entity in place, violating immutability principle
- **Location**: `src/app/features/user/application/use_cases/update_user.py`
- **Lines**: 48-55
- **Link**: [`update_user.py:48-55`](../src/app/features/user/application/use_cases/update_user.py#L48-L55)
- **Skill**: clean-architecture (Entity Purity)
- **Description**: The use case fetches an existing `UserEntity`, then directly mutates its attributes (`existing_user.email = ...`, `existing_user.first_name = ...`). Domain entities should generally be immutable or use explicit methods for updates. Directly mutating fields breaks encapsulation and makes it hard to track changes.
- **Evidence**:
```python
existing_user = await self.user_repository.find_by_id(user_uuid)

# Apply partial updates (only non-None fields)
if user_update.email is not None:
    existing_user.email = Email(user_update.email)  # ← Direct mutation

if user_update.first_name is not None:
    existing_user.first_name = user_update.first_name  # ← Direct mutation
```
- **Impact**: 
  - Breaks domain integrity — no single place validates an update operation
  - If business rules apply to updates (e.g., "cannot change email if account is locked"), there's no encapsulated place to enforce them
  - Makes debugging harder — can't tell where entity state was changed
- **Remediation**: Add an `update()` method on `UserEntity` that encapsulates update logic:
```python
# In UserEntity
def update_profile(self, email: Optional[Email], first_name: Optional[str], last_name: Optional[str]) -> None:
    if email:
        self.email = email
    if first_name:
        self.first_name = first_name
    if last_name:
        self.last_name = last_name
    self.updated_at = get_current_datetime()
```
Then in the use case:
```python
existing_user.update_profile(
    email=Email(user_update.email) if user_update.email else None,
    first_name=user_update.first_name,
    last_name=user_update.last_name
)
```

---

### [H-04] Dependency on SQLAlchemy in retry decorator violates Clean Architecture dependency rule
- **Location**: `src/shared/utils/retry_decorator.py`
- **Lines**: 39-41, 66-68
- **Links**: 
  - [`retry_decorator.py:39-41`](../src/shared/utils/retry_decorator.py#L39-L41)
  - [`retry_decorator.py:66-68`](../src/shared/utils/retry_decorator.py#L66-L68)
- **Skill**: clean-architecture (Dependency Rule)
- **Description**: The `retry_read_operation` and `retry_write_operation` decorators in the **shared utilities layer** (which should be framework-agnostic) import SQLAlchemy-specific exceptions (`SQLAlchemyError`, `OperationalError`, `IntegrityError`) directly. This couples core infrastructure utilities to a specific ORM, violating the dependency rule.
- **Evidence**:
```python
# retry_decorator.py, lines 39-41
if exceptions is None:
    from sqlalchemy.exc import SQLAlchemyError, OperationalError
    exceptions = (SQLAlchemyError, OperationalError, TimeoutError)
```
- **Impact**: 
  - If you ever swap ORMs (e.g., move to raw asyncpg, or add a MongoDB adapter), this utility breaks
  - The shared layer is now infrastructure-aware, reducing its reusability
  - Violates Clean Architecture's principle that inner layers should know nothing about outer layer frameworks
- **Remediation**: Move these decorators to `src/shared/infrastructure/postgres/` or make them generic by accepting `exceptions` as a required parameter rather than defaulting to SQLAlchemy types. Alternatively, define a custom domain exception hierarchy and catch only those:
```python
# Define in shared/domain/exceptions/
class RepositoryError(Exception): pass
class IntegrityConstraintViolation(RepositoryError): pass

# Catch in repository implementations and re-raise as domain exceptions
try:
    # ... SQLAlchemy code
except IntegrityError as e:
    raise IntegrityConstraintViolation(...) from e
```

---

### [H-05] No domain events for critical state changes
- **Location**: `src/app/features/user/domain/entities/user_entity.py` and use cases
- **Lines**: N/A (missing implementation)
- **Link**: `src/app/features/user/domain/events/` ← **CREATE THIS DIRECTORY**
- **Skill**: domain-driven-design (DE — Domain Events)
- **Description**: The User aggregate undergoes significant state changes (user created, user deleted, role changed, email changed, account deactivated) but **no domain events are raised**. This prevents other parts of the system from reacting to these changes (e.g., sending welcome emails, audit logging, invalidating caches, notifying admins of role changes).
- **Evidence**: 
  - No `events/` directory exists in `src/app/features/user/domain/`
  - No event publishing mechanism in `UserEntity`
  - Use cases perform state changes with no event emission
  - File search for `*_event*.py` returned zero results
- **Impact**: 
  - **No audit trail** — cannot track who was promoted to admin or when users were deactivated
  - **Tight coupling** — if you later need to send an email on user creation, you have to modify the use case directly
  - **Lost business opportunities** — cannot build features like "welcome email," "password change notification," or "admin activity log" without invasive code changes
  - **Harder to scale** — cannot offload side effects to async workers/event handlers
- **Remediation**: Introduce domain events following DDD event sourcing patterns:

**Step 1: Create domain event base and specific events**
```python
# src/app/features/user/domain/events/base_event.py
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class DomainEvent:
    aggregate_id: UUID
    occurred_at: datetime

# src/app/features/user/domain/events/user_events.py
from dataclasses import dataclass
from src.app.features.user.domain.events.base_event import DomainEvent

@dataclass(frozen=True)
class UserCreated(DomainEvent):
    email: str
    role: str

@dataclass(frozen=True)
class UserDeactivated(DomainEvent):
    reason: str

@dataclass(frozen=True)
class UserRoleChanged(DomainEvent):
    old_role: str
    new_role: str

@dataclass(frozen=True)
class UserEmailChanged(DomainEvent):
    old_email: str
    new_email: str
```

**Step 2: Add event collection to entity**
```python
class UserEntity(BaseEntity):
    def __init__(self, ...):
        # ...existing init...
        self._domain_events: List[DomainEvent] = []

    def collect_events(self) -> List[DomainEvent]:
        """Retrieve and clear collected events."""
        events = self._domain_events.copy()
        self._domain_events.clear()
        return events

    def deactivate(self, reason: str = "User requested") -> None:
        if self.role.is_admin:
            raise ValueError("Cannot deactivate admin users")
        self.is_active = False
        self._mark_updated()
        # Raise domain event
        self._domain_events.append(UserDeactivated(
            aggregate_id=self.id.value,
            occurred_at=get_current_datetime(),
            reason=reason
        ))
```

**Step 3: Publish events in use cases**
```python
# In SaveUser use case:
saved_user = await self.user_repository.save(user_entity)
events = saved_user.collect_events()
for event in events:
    await self.event_publisher.publish(event)
```

---

### [H-06] Entity properties are publicly mutable, breaking encapsulation
- **Location**: `src/app/features/user/domain/entities/user_entity.py`
- **Lines**: 25-30
- **Link**: [`user_entity.py:25-30`](../src/app/features/user/domain/entities/user_entity.py#L25-L30)
- **Skill**: domain-driven-design (ENT — Entity)
- **Description**: All properties of `UserEntity` (`email`, `first_name`, `last_name`, `hashed_password`, `role`, `is_active`) are public attributes with no access control. Any external code can directly mutate them without going through domain methods, bypassing invariant checks and business rules.
- **Evidence**:
```python
# Current: anyone can do this
user.is_active = False  # No validation, no event, no audit trail
user.role = Role.ADMIN  # Promotion with no authorization check
user.email = Email("attacker@evil.com")  # Email change with no uniqueness check
```
All assignments happen in `__init__` as direct attribute assignments with no property decorators or setters.
- **Impact**: 
  - **Invariants cannot be enforced** — nothing prevents invalid state like `is_active=False` with `role=ADMIN` if a business rule forbids that
  - **No change tracking** — mutations bypass `_mark_updated()` or event publishing
  - **Business rules scattered** — validation for "can change email?" is in the use case instead of the entity
  - **Testing is incomplete** — you can't test the entity in isolation because it has no behavior to test
- **Remediation**: Make attributes private and expose them through properties or explicit methods:

**Option 1: Python properties (read-only external access)**
```python
class UserEntity(BaseEntity):
    def __init__(self, ...):
        self._email = email
        self._first_name = first_name
        self._last_name = last_name
        self._hashed_password = hashed_password
        self._role = role
        self._is_active = is_active
        # ...

    @property
    def email(self) -> Email:
        return self._email

    @property
    def role(self) -> Role:
        return self._role

    @property
    def is_active(self) -> bool:
        return self._is_active

    # Mutations only through domain methods
    def change_email(self, new_email: Email) -> None:
        self._email = new_email
        self._mark_updated()

    def promote_to_admin(self) -> None:
        if self._role.is_admin:
            raise ValueError("Already admin")
        self._role = Role.ADMIN
        self._mark_updated()
```

**Option 2: Dataclass with `frozen=True` and factory methods** (more pythonic but requires rethinking mutability)

---

### [H-07] No explicit aggregate boundary — User treated as standalone entity
- **Location**: `src/app/features/user/domain/entities/`
- **Lines**: N/A (architectural gap)
- **Link**: [`user/domain/entities/`](../src/app/features/user/domain/entities/)
- **Skill**: domain-driven-design (AGG — Aggregate)
- **Description**: The `UserEntity` is not explicitly marked as an **Aggregate Root**, and there's no documentation or enforcement of aggregate boundaries. If the domain evolves to include related entities (e.g., `UserProfile`, `UserPreferences`, `UserSession`), there's currently no guidance on whether they should be separate aggregates or children of the `User` aggregate.
- **Evidence**:
  - No `AggregateRoot` marker interface or base class
  - No documentation defining what the User aggregate controls
  - Repository directly exposes `UserEntity` with no concept of "root"
  - No consistency boundary enforcement
- **Impact**: Low severity now (only one entity in the User context), but **high risk for future complexity**:
  - If you add `UserProfile` as a separate entity, should it be in the same aggregate or a different one?
  - If a user has multiple `UserSession` entities, can they be modified independently or only through the User root?
  - Without clear boundaries, developers will make inconsistent decisions leading to data integrity issues
- **Remediation**: 
  1. **Mark `UserEntity` as aggregate root** by inheriting from `AggregateRoot` base class:
```python
# src/shared/domain/entities/aggregate_root.py
class AggregateRoot(BaseEntity):
    """Marker for aggregate roots. Only roots are referenced by repositories."""
    pass

# src/app/features/user/domain/entities/user_entity.py
class UserEntity(AggregateRoot):  # ← Changed from BaseEntity
    # ...
```
  2. **Document aggregate invariants** in entity docstring:
```python
class UserEntity(AggregateRoot):
    """
    User Aggregate Root.
    
    Aggregate boundary: User entity only. User preferences/sessions are 
    separate aggregates referenced by UserID.
    
    Invariants enforced:
    - Email must be unique across all users (enforced by repository)
    - Admin users cannot be deactivated
    - Only active users can be promoted to admin
    """
```
  3. **Enforce repository rule**: "One repository per aggregate root." Currently correct (only `UserRepository` exists), but codify it in guidelines.

---

## Medium Priority Issues

### [M-01] Mutable default argument in `BaseEntity.__init__`
- **Location**: `src/shared/domain/entities/base_entity.py`
- **Lines**: 10-13
- **Link**: [`base_entity.py:10-13`](../src/shared/domain/entities/base_entity.py#L10-L13)
- **Skill**: python-standards (Idiomatic Python)
- **Description**: The `__init__` method has `id: EntityId = None` as a default. While this specific case is safe because the default is `None` (immutable), the pattern is often a source of bugs when defaults are mutable (lists, dicts). However, the real issue here is that `EntityId` should not have `None` as a valid type — it should be `Optional[EntityId]` explicitly.
- **Evidence**:
```python
def __init__(self,
             id: EntityId = None,  # ← Type hint says EntityId, default is None
             created_at: Optional[datetime] = None,
             updated_at: Optional[datetime] = None
             ):
```
- **Impact**: Type checkers (mypy, pyright) will flag this as an error — the type annotation says `EntityId` but the default is `None`. Should be `Optional[EntityId]` or `EntityId | None`.
- **Remediation**:
```python
def __init__(self,
             id: Optional[EntityId] = None,
             created_at: Optional[datetime] = None,
             updated_at: Optional[datetime] = None
             ):
```

---

### [M-02] No structured logging — plain string formatting
- **Location**: Throughout the codebase
- **Examples**: 
  - `src/app/features/user/infrastructure/postgres/repository/user_repository_impl.py:43`
  - `src/app/features/user/application/use_cases/save_user.py:36`
- **Links**: 
  - [`user_repository_impl.py:43`](../src/app/features/user/infrastructure/postgres/repository/user_repository_impl.py#L43)
  - [`save_user.py:36`](../src/app/features/user/application/use_cases/save_user.py#L36)
- **Skill**: python-standards (Logging)
- **Description**: The codebase uses plain string message logging (`log.info(f"User with email {email.value} found.")`) instead of structured logging. For production services, structured logging (key-value pairs) is critical for log aggregation, querying, and monitoring.
- **Evidence**:
```python
# user_repository_impl.py, line 43
log.info(f"User with email {email.value} found.")

# save_user.py, line 36
log.info(saved_user.first_name)  # ← Logs a raw value with no context
```
- **Impact**: 
  - Logs are hard to query in production monitoring tools (Datadog, Splunk, CloudWatch)
  - No correlation IDs or request context
  - Performance: f-strings are evaluated even if log level is disabled
- **Remediation**: Adopt structured logging with `structlog` or use lazy evaluation:
```python
# Option 1: Lazy evaluation
log.info("User found by email", extra={"email": email.value, "user_id": str(user_id)})

# Option 2: Use structlog
import structlog
log = structlog.get_logger()
log.info("user_found", email=email.value, user_id=str(user_id))
```

---

### [M-03] `HashedPassword` hashing logic in domain layer (potential SRP violation)
- **Location**: `src/app/features/user/domain/value_objects/hashed_password.py`
- **Lines**: 43-70 (factory method), 72-84 (verify method)
- **Link**: [`hashed_password.py`](../src/app/features/user/domain/value_objects/hashed_password.py)
- **Skill**: solid-principles (SRP), clean-architecture (Entity Purity — borderline)
- **Description**: The `HashedPassword` value object contains bcrypt hashing logic (`from_plain_text()`, `verify()`). While value objects can perform validation, **cryptographic operations** (hashing, verification) are arguably infrastructure concerns, not domain logic. The domain should know "a password is hashed," but not "how to hash with bcrypt."
- **Evidence**:
```python
@classmethod
def from_plain_text(cls, plain_password: str) -> "HashedPassword":
    # ... validation ...
    salt = bcrypt.gensalt(rounds=_BCRYPT_ROUNDS)  # ← Infrastructure: bcrypt
    hashed = bcrypt.hashpw(password_bytes, salt)
    return cls(value=hashed.decode("utf-8"))

def verify(self, plain_password: str) -> bool:
    return bcrypt.checkpw(password_bytes, hashed_bytes)  # ← Infrastructure: bcrypt
```
- **Impact**: 
  - If you need to change hashing algorithms (e.g., switch to Argon2), you must modify a domain value object
  - Cannot easily swap hashing strategies without touching domain code
  - The domain layer now depends on `bcrypt`, a third-party library
- **Remediation**: Extract hashing to an infrastructure service:
```python
# src/shared/infrastructure/security/password_hasher.py
from abc import ABC, abstractmethod

class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, plain_password: str) -> str: pass
    
    @abstractmethod
    def verify(self, plain_password: str, hashed: str) -> bool: pass

class BcryptPasswordHasher(PasswordHasher):
    def hash(self, plain_password: str) -> str:
        # ... bcrypt logic here
    
    def verify(self, plain_password: str, hashed: str) -> bool:
        # ... bcrypt verify here
```
Then inject the hasher into the use case. The domain value object becomes a simple wrapper:
```python
@dataclass(frozen=True)
class HashedPassword:
    value: str
    # No hashing logic — just validation that it looks like a hash
```

**Severity rationale**: Marked Medium because the code works and is testable. Moving to High would require evidence that it's actively causing issues.

---

### [M-04] Commented-out code in route handlers
- **Location**: `src/app/features/user/presentation/web/routes/user_routes.py`
- **Lines**: 15-23, 30-36
- **Links**: 
  - [`user_routes.py:15-23`](../src/app/features/user/presentation/web/routes/user_routes.py#L15-L23)
  - [`user_routes.py:30-36`](../src/app/features/user/presentation/web/routes/user_routes.py#L30-L36)
- **Skill**: dry-kiss-yagni (YAGNI)
- **Description**: Docstrings are commented out in two route handlers (`get_user_by_id`, `create_user`). Commented code is a YAGNI smell — if it's not needed, delete it. If it's needed, uncomment it. Keeping it commented "just in case" adds clutter.
- **Evidence**:
```python
@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: UUID, user_service: UserService = Depends(get_user_service)) -> UserResponse:
    # """
    # Get a user by their ID.
    # Args: ...
    # Returns: ...
    # """
```
- **Impact**: Minor — adds visual clutter, suggests code is in an uncertain state. Inconsistent with other endpoints that have active docstrings.
- **Remediation**: Uncomment the docstrings (they're useful for OpenAPI docs) or remove them entirely if they're redundant with type hints and response models.

---

### [M-05] Unpinned dependencies in `requirements.txt`
- **Location**: `requirements.txt`
- **Link**: [`requirements.txt`](../requirements.txt)
- **Skill**: python-standards (Dependency Management)
- **Description**: While most dependencies are pinned to specific versions (good), there's no lock file (`requirements.lock` or `poetry.lock`). This means transitive dependencies are not locked, leading to non-reproducible builds.
- **Evidence**:
```
fastapi==0.115.11  # ← Pinned (good)
uvicorn==0.34.0    # ← Pinned (good)
# But: transitive deps (e.g., pydantic-core, starlette, anyio) are NOT locked
```
- **Impact**: 
  - `pip install -r requirements.txt` on two different days can produce different environments if a transitive dependency releases a new version
  - Security: cannot audit exact versions of all dependencies
  - Difficult to reproduce production bugs in dev environment
- **Remediation**: Use `pip-tools` with `requirements.in` → `requirements.txt` compile step, or migrate to Poetry:
```bash
# With pip-tools:
pip install pip-tools
echo "fastapi==0.115.11" > requirements.in
pip-compile requirements.in  # Generates requirements.txt with locked transitive deps
```

---

### [M-06] Role validation in use case instead of value object
- **Location**: 
  - `src/app/features/user/application/dtos/user_dto.py:30`
  - `src/app/features/user/application/use_cases/save_user.py:22`
- **Links**: 
  - [`user_dto.py:30`](../src/app/features/user/application/dtos/user_dto.py#L30)
  - [`save_user.py:22`](../src/app/features/user/application/use_cases/save_user.py#L22)
- **Skill**: clean-architecture (Entity Purity)
- **Description**: The `SaveUser` use case constructs a `Role` value object using `Role.from_str(user_create.role)`. This is correct. However, the `UserCreate` DTO accepts `role: str` as a plain string with a default `"user"`. Validation only happens when the use case executes, not at the API boundary.
- **Evidence**:
```python
# user_dto.py
class UserCreate(BaseModel):
    role: str = "user"  # ← Accepts any string; validated later

# save_user.py, line 22
role_vo = Role.from_str(user_create.role)  # ← Validation deferred to use case
```
- **Impact**: 
  - Invalid roles pass through the controller and reach the use case before being rejected
  - FastAPI's automatic OpenAPI docs won't show the valid role enum values — just "string"
  - Error handling is delayed, making debugging harder
- **Remediation**: Use Pydantic's `Literal` or a custom validator in the DTO:
```python
from typing import Literal

class UserCreate(BaseModel):
    role: Literal["admin", "user"] = "user"
```
Or use Pydantic's enum support:
```python
from enum import Enum as PyEnum

class RoleDTO(str, PyEnum):
    ADMIN = "admin"
    USER = "user"

class UserCreate(BaseModel):
    role: RoleDTO = RoleDTO.USER
```

---

### [M-07] No database connection health check in `/health` endpoint
- **Location**: `src/app/app.py`
- **Lines**: 41-43
- **Link**: [`app.py:41-43`](../src/app/app.py#L41-L43)
- **Skill**: kiss-yagni (KISS — overly simple health check)
- **Description**: The `/health` endpoint returns a static `"Ok"` string without verifying that critical dependencies (database, external services) are actually reachable. This is not a true health check.
- **Evidence**:
```python
@fastApiApp.get("/health")
def get_health_check():
    return "Ok"  # ← Always returns Ok, even if DB is down
```
- **Impact**: 
  - Load balancers / orchestrators (Kubernetes, ECS) think the app is healthy even when it can't serve requests
  - Operations teams have no visibility into dependency health
- **Remediation**: Add a database connection check:
```python
@fastApiApp.get("/health")
async def get_health_check(session: AsyncSession = Depends(get_database_session)):
    try:
        await session.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail={"status": "unhealthy", "database": str(e)})
```

---

### [M-08] `get_database_session()` dependency creates a new connection manager on every request
- **Location**: `src/app/features/user/presentation/web/dependencies.py`
- **Lines**: 14-22
- **Link**: [`dependencies.py:14-22`](../src/app/features/user/presentation/web/dependencies.py#L14-L22)
- **Skill**: solid-principles (DIP), python-standards (Performance)
- **Description**: The `get_database_session()` dependency instantiates a new `PostgresDbConnection` on every request. This is inefficient — the connection manager (with its engine and session factory) should be created once at app startup and reused.
- **Evidence**:
```python
async def get_database_session() -> AsyncGenerator[Any, Any]:
    postgres_config = get_config_value(app_config, "postgres", {})
    postgres_db_session_manager = PostgresDbConnection(postgres_config)  # ← New instance every request!

    async with postgres_db_session_manager.get_session() as session:
        yield session
```
- **Impact**: 
  - Performance: wasteful object creation on every request
  - Potential connection pool issues if the engine isn't properly shared
  - Not a severe runtime issue because the engine internally pools, but violates best practices
- **Remediation**: Create the connection manager once at app startup and store it in app state:
```python
# In app.py
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    postgres_config = get_config_value(app_config.config, "postgres", {})
    app.state.db = PostgresDbConnection(postgres_config)
    yield
    # Shutdown
    await app.state.db.close_engine()

fastApiApp = FastAPI(title=app_name, version=app_version, lifespan=lifespan)

# In dependencies.py
async def get_database_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    async with request.app.state.db.get_session() as session:
        yield session
```

---

### [M-09] Business rule enforcement in use case instead of entity
- **Location**: `src/app/features/user/application/use_cases/save_user.py`
- **Lines**: 17-33
- **Link**: [`save_user.py:17-33`](../src/app/features/user/application/use_cases/save_user.py#L17-L33)
- **Skill**: domain-driven-design (ASVC — Application Service / Use-Case)
- **Description**: The `SaveUser` use case constructs the `UserEntity` by manually assembling value objects (`Email`, `HashedPassword`, `Role`) and setting `is_active=True`. This logic — **"new users are always active by default"** — is a business rule that belongs in the domain entity as a factory method, not in the application layer.
- **Evidence**:
```python
# save_user.py (use case)
entity_id = EntityId.generate()
email_vo = Email(user_create.email)
role_vo = Role.from_str(user_create.role)
hashed_password_vo = HashedPassword.from_plain_text(user_create.password)

user_entity = UserEntity(
    id=entity_id,
    email=email_vo,
    first_name=user_create.first_name,
    last_name=user_create.last_name,
    hashed_password=hashed_password_vo,
    role=role_vo,
    is_active=True,  # ← Business rule: new users are active
)
```
The rule "new users start as active" is repeated in every place that creates a user (if there are multiple creation flows, this will duplicate).
- **Impact**: 
  - Business rule is **not discoverable** — reading `UserEntity` doesn't tell you that users default to active
  - **Duplication risk** — if a second signup flow exists (e.g., admin-created users), it may forget to set `is_active=True`
  - **Harder to change** — if the rule changes to "new users start inactive pending email verification," you must find all use cases instead of changing one factory method
- **Remediation**: Move user construction to a static factory method in `UserEntity`:
```python
# user_entity.py
class UserEntity(BaseEntity):
    @staticmethod
    def create_new_user(
        email: Email,
        first_name: str,
        last_name: str,
        password: HashedPassword,
        role: Role = Role.USER
    ) -> "UserEntity":
        """
        Factory method for creating a new user.
        Business rules:
        - New users are always active
        - Default role is USER unless specified
        - ID and timestamps are auto-generated
        """
        return UserEntity(
            id=EntityId.generate(),
            email=email,
            first_name=first_name,
            last_name=last_name,
            hashed_password=password,
            role=role,
            is_active=True,  # ← Business rule centralized here
            created_at=None,  # Auto-filled by BaseEntity
            updated_at=None
        )
```
Then simplify the use case:
```python
# save_user.py (use case)
user_entity = UserEntity.create_new_user(
    email=Email(user_create.email),
    first_name=user_create.first_name,
    last_name=user_create.last_name,
    password=HashedPassword.from_plain_text(user_create.password),
    role=Role.from_str(user_create.role)
)
```

---

### [M-10] Missing equality implementation based on identity
- **Location**: `src/app/features/user/domain/entities/user_entity.py`
- **Lines**: N/A (missing methods)
- **Link**: [`user_entity.py`](../src/app/features/user/domain/entities/user_entity.py)
- **Skill**: domain-driven-design (ENT — Entity)
- **Description**: `UserEntity` does not implement `__eq__` and `__hash__` methods. In DDD, **entities are equal if their IDs are equal**, regardless of attribute values. Without explicit equality, Python defaults to reference equality (`id()` of the object), which breaks entity comparisons across repository fetches or after updates.
- **Evidence**:
```python
class UserEntity(BaseEntity):
    # ...no __eq__ or __hash__ methods
```
This means:
```python
user1 = await repo.find_by_id(some_id)
user2 = await repo.find_by_id(some_id)
assert user1 == user2  # ❌ FAILS — different object instances
assert user1 is user2  # ❌ FAILS — not the same reference

# Expected behavior:
assert user1.id == user2.id  # ✅ True
assert user1 == user2        # ❌ False (because __eq__ not implemented)
```
- **Impact**: 
  - **Cannot use entities in sets or as dict keys** — hash is based on object reference, not ID
  - **Comparison logic is verbose** — must always compare `.id.value` explicitly
  - **Violates DDD principle** — entities should be equal by identity, not reference
- **Remediation**: Add identity-based equality to `BaseEntity` (so all entities inherit it):
```python
# base_entity.py
class BaseEntity:
    # ...existing code...

    def __eq__(self, other: object) -> bool:
        """Entities are equal if their IDs are equal."""
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash based on ID for use in sets/dicts."""
        return hash(self.id)
```
Now:
```python
user1 = await repo.find_by_id(some_id)
user2 = await repo.find_by_id(some_id)
assert user1 == user2  # ✅ True (same ID)
assert user1 is user2  # ❌ False (different objects, which is fine)

users = {user1, user2}  # ✅ Set has 1 element (deduplicated by ID)
```

---

## Low Priority Issues

### [L-01] Inconsistent import ordering
- **Location**: Multiple files
- **Examples**: 
  - `src/app/app.py:1-7`
  - `src/app/features/user/presentation/web/routes/user_routes.py:1-8`
- **Links**: 
  - [`app.py:1-7`](../src/app/app.py#L1-L7)
  - [`user_routes.py:1-8`](../src/app/features/user/presentation/web/routes/user_routes.py#L1-L8)
- **Skill**: python-standards (PEP 8)
- **Description**: Imports are not consistently ordered into stdlib, third-party, and local groups with blank lines between them. PEP 8 recommends this grouping.
- **Evidence**:
```python
# app.py
import os  # stdlib
from fastapi import FastAPI  # third-party
from fastapi.middleware.cors import CORSMiddleware  # third-party
from src.app.config.app_config import AppConfig  # local — no blank line separating groups
```
- **Impact**: Minor readability issue. Makes it harder to scan import sections.
- **Remediation**: Use an auto-formatter like `ruff` or `isort`:
```bash
pip install ruff
ruff check --select I --fix .
```

---

### [L-02] Missing `__repr__` methods on domain entities
- **Location**: 
  - `src/shared/domain/entities/base_entity.py`
  - `src/app/features/user/domain/entities/user_entity.py`
- **Links**: 
  - [`base_entity.py`](../src/shared/domain/entities/base_entity.py)
  - [`user_entity.py`](../src/app/features/user/domain/entities/user_entity.py)
- **Skill**: python-standards (Idiomatic Python)
- **Description**: Domain entities don't define `__repr__` methods. This makes debugging harder — when you print an entity instance in logs or a debugger, you get the default `<UserEntity object at 0x...>` instead of useful information.
- **Evidence**: No `__repr__` defined in `BaseEntity` or `UserEntity`.
- **Impact**: Harder to debug. Log statements that include entities show useless memory addresses.
- **Remediation**: Add `__repr__` methods:
```python
class UserEntity(BaseEntity):
    # ... existing code ...
    
    def __repr__(self) -> str:
        return f"UserEntity(id={self.id}, email={self.email}, role={self.role})"
```

---

### [L-03] Boolean field naming inconsistency
- **Location**: `src/app/features/user/domain/entities/user_entity.py` (line 21), `user_model.py` (line 21)
- **Skill**: python-standards (Naming Conventions)
- **Description**: The boolean field is named `is_active` (correct predicate form), but used inconsistently. In the DTO layer, it's also `is_active`. However, the convention check is just a quality note — it IS correctly named. **Retracted — no issue here.**
- **Remediation**: None needed — naming is correct.

---

### [L-04] Log level configured from environment variable without validation
- **Location**: `src/shared/utils/log_util.py`
- **Line**: 6
- **Link**: [`log_util.py:6`](../src/shared/utils/log_util.py#L6)
- **Skill**: python-standards (Error Handling)
- **Description**: The `LOG_LEVEL` is read from an environment variable and uppercased, but there's no validation that it's a valid log level. If someone sets `LOG_LEVEL=INVALID`, the logger will fail silently or use a default.
- **Evidence**:
```python
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logger.setLevel(log_level)  # ← No validation; if invalid, setLevel may raise
```
- **Impact**: Minor — misconfiguration could cause silent failures or unexpected behavior.
- **Remediation**: Validate the log level:
```python
import logging

_VALID_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
if LOG_LEVEL not in _VALID_LEVELS:
    LOG_LEVEL = "INFO"
logger.setLevel(getattr(logging, LOG_LEVEL))
```

---

### [L-05] `uuid.uuid1()` used instead of `uuid4()` for primary keys
- **Location**: `src/shared/infrastructure/postgres/models/base_model.py`
- **Line**: 22
- **Link**: [`base_model.py:22`](../src/shared/infrastructure/postgres/models/base_model.py#L22)
- **Skill**: python-standards (Security Hygiene — minor)
- **Description**: The `BaseModel` uses `uuid.uuid1()` as the default for primary keys. UUID1 includes the MAC address and timestamp, making it **partially predictable** and leaking information about the server. UUID4 is random and preferred for most use cases.
- **Evidence**:
```python
id = Column(
    UUID(as_uuid=True),
    primary_key=True,
    default=uuid.uuid1,  # ← Uses UUID1 (MAC address + timestamp)
    unique=True,
)
```
- **Impact**: 
  - Low security risk: leaks server MAC address and creation timestamp
  - UUIDs are slightly predictable (can guess the next one within a time window)
- **Remediation**: Change to `uuid.uuid4()`:
```python
default=uuid.uuid4,
```

---

### [L-06] Hardcoded CORS origins in production code
- **Location**: `src/app/app.py`
- **Lines**: 23-25
- **Link**: [`app.py:23-25`](../src/app/app.py#L23-L25)
- **Skill**: python-standards (Security Hygiene)
- **Description**: CORS origins are hardcoded to `["http://localhost"]` directly in the app code, with a comment suggesting they should come from config. This is commented as "from config" but actually uses a hardcoded list.
- **Evidence**:
```python
# --- CORS Origins from config ---
origins = [
    "http://localhost"  # ← Hardcoded; should read from config
]
```
- **Impact**: Low in development. In production, this would need to be changed. The comment indicates intent to read from config but it's not implemented.
- **Remediation**: Read from config:
```python
origins = config.get_config("cors.origins", ["http://localhost"])
```
And add to `config_*.yml`:
```yaml
cors:
  origins:
    - "http://localhost:3000"
    - "https://yourdomain.com"
```

---

### [L-07] Technical name "UserService" instead of domain-driven name
- **Location**: `src/app/features/user/application/services/user_service.py`
- **Lines**: 8
- **Link**: [`user_service.py:8`](../src/app/features/user/application/services/user_service.py#L8)
- **Skill**: domain-driven-design (UL — Ubiquitous Language)
- **Description**: The class is named `UserService`, which is a generic technical term that appears in every CRUD application. In DDD, even application services should use **ubiquitous language** from the domain. Names like `UserManagement`, `UserAccountService`, or simply removing it in favor of direct use case injection would align better with domain vocabulary.
- **Evidence**:
```python
class UserService:
    # Purely technical name, no domain meaning
```
Compare to domain-driven alternatives:
- `UserAccountManagement` — clearer purpose
- `UserRegistration` — if focused on signup flows
- Or remove it entirely and inject use cases directly (already flagged in H-01)
- **Impact**: Low severity — this is a naming issue, not a functional defect. However:
  - **Ubiquitous language erosion** — "service" is developer jargon, not domain language
  - **Generic names breed generic thinking** — developers see "service" and dump random logic there
- **Remediation**: Since H-01 already recommends removing `UserService` entirely, this is automatically resolved by that fix. If you choose to keep a service layer, rename to domain-specific terminology:
```python
# Option 1: Remove (recommended per H-01)
# Inject use cases directly into routes

# Option 2: Rename to domain term
class UserAccountManagement:
    """Manages user account lifecycle: registration, profile updates, deactivation."""
```

---

## Follow-up Steps

1. **[Critical — C-01]** Establish test suite immediately. Start with critical paths: save user, get user by ID, authentication (if exists). Aim for 70%+ coverage before next deployment.

2. **[Critical — C-02]** Create `pyproject.toml` to modernize packaging, centralize tool config, and properly separate dev/prod dependencies.

3. **[Critical — C-03]** Fix broad exception handling in `user_repository_impl.py` — replace `except Exception` with specific SQLAlchemy exceptions (`IntegrityError`, `OperationalError`, `SQLAlchemyError`).

4. **[Critical — C-04]** Address Anemic Domain Model — add domain methods to `UserEntity` (`change_email()`, `deactivate()`, `promote_to_admin()`, `update_profile()`, etc.) to encapsulate business logic and protect invariants.

5. **[High — H-01]** Remove or justify `UserService` pass-through layer. If kept, add actual orchestration logic; otherwise inject use cases directly into routes.

6. **[High — H-05]** Introduce domain events for critical state changes (user created, deleted, role changed, deactivated). Create event base classes and publishing mechanism.

7. **[High — H-06]** Make entity properties private with property decorators to enforce encapsulation and prevent direct external mutation.

8. **[High — H-07]** Explicitly mark `UserEntity` as aggregate root and document aggregate boundaries/invariants for future domain expansion.

9. **[Medium — All Medium findings]** Address missing type hints, dependency rule violations, duplicated SQL session management, hardcoded config values, and refactor business rule construction into domain factory methods.

10. **[Low — All Low findings]** Clean up commented code, improve logging consistency, fix hardcoded CORS origins, rename technical classes to domain-driven names.

**Recommended sprint plan:**
- **Sprint 1 (Critical):** C-01 (tests), C-02 (pyproject.toml), C-03 (exception handling), C-04 (add domain methods)
- **Sprint 2 (High):** H-05 (domain events), H-06 (encapsulation), H-07 (aggregate boundary), H-01 (remove UserService)
- **Sprint 3 (Medium/Low):** Type hints, refactoring, documentation improvements

2. **[Critical — C-02]** Create `pyproject.toml` with proper project metadata, dependencies, and tool configuration. Migrate from bare `requirements.txt` to proper packaging.

3. **[Critical — C-03]** Refactor exception handling in repository layer to catch specific SQLAlchemy exceptions instead of bare `Exception`.

4. **[High — H-01]** Remove `UserService` layer or add explicit business value (composition, cross-cutting concerns). If it's a pure pass-through, inject use cases directly.

5. **[High — H-02]** Add return type annotations to all service and use-case methods. Run `mypy` to catch type errors.

6. **[High — H-03]** Refactor `UpdateUserUseCase` to use an entity method for updates instead of direct field mutation.

7. **[High — H-04]** Move SQLAlchemy-specific retry logic out of shared utilities. Define domain exceptions or make decorators generic.

8. **[Medium — M-01 through M-08]** Address type hint corrections, structured logging, dependency management, health check improvements, and performance optimizations in the dependency injection layer.

9. **[Low — L-01 through L-06]** Code quality improvements: import ordering, `__repr__` methods, log level validation, UUID generation strategy, and CORS configuration.

10. **[Documentation]** Document architecture decisions in an `ADR/` (Architecture Decision Records) folder. Specifically:
    - Why Clean Architecture layers are chosen
    - Repository vs Active Record pattern choice
    - Value object philosophy
    - Test strategy (once established)

---

## Audit Metadata

| Field | Value |
|---|---|
| Audit version | V1 (updated with DDD skill) |
| Date | April 16, 2026 (Updated: April 26, 2026) |
| Skills applied | clean-architecture, dry-kiss-yagni, python-standards, solid-principles, domain-driven-design |
| Files scanned | 69 Python files |
| Python version (detected) | 3.10+ (FastAPI 0.115.11, Pydantic 2.10.6) |
| Project type | FastAPI REST API with Clean Architecture, PostgreSQL, SQLAlchemy 2.0 |
| Auditor agent | code-auditor v2.0.0 |
| Total findings | 27 (4 Critical, 7 High, 9 Medium, 7 Low) |

---

## Architecture Assessment

The project demonstrates a **solid understanding of Clean Architecture principles** with clear layer separation:

- **Domain layer** (`domain/entities`, `domain/value_objects`, `domain/repositories`) — Well-defined, mostly pure. Value objects enforce business rules. Repository abstractions are correctly placed.
- **Application layer** (`application/use_cases`, `application/services`, `application/dtos`) — Use cases encapsulate business flows. DTOs separate API contracts from domain.
- **Infrastructure layer** (`infrastructure/postgres`) — Correctly isolated. ORM models are separate from domain entities.
- **Presentation layer** (`presentation/web/routes`) — Thin adapters. Routes delegate to services/use cases.

**Strengths:**
- Clear separation between domain entities and ORM models with explicit mappers
- Repository pattern with abstractions in domain layer, implementations in infrastructure
- Value objects with validation (Email, HashedPassword, Role, EntityId)
- Async/await used consistently throughout
- Dependency injection via FastAPI's `Depends` system
- Pydantic v2 for DTOs with proper configuration

**Weaknesses:**
- **No tests** (critical gap — zero test coverage)
- **Anemic domain model** — entities have no behavior, all logic in use cases
- **No domain events** — missing event-driven patterns for state changes
- **Public entity properties** — no encapsulation or invariant protection
- **Service layer adds no value** (pure pass-through to use cases)
- **Missing modern Python packaging** (`pyproject.toml`)
- **Some dependency rule violations** (shared utils importing SQLAlchemy)
- **No aggregate boundaries** defined for future domain expansion

**Overall Grade: C+** (originally B-, downgraded after DDD audit)

The architecture follows Clean Architecture **structure** well (layers, dependencies) but violates DDD **principles** (anemic model, missing events, no encapsulation). With proper domain behavior, domain events, tests, and packaging, this would be an A-level reference implementation.

