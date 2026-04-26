---
name: clean-architecture
description: Audits for Clean Architecture violations — dependency rule, layer separation, entity purity, use-case isolation, adapter/interface boundaries.
version: 1.0.0
tags: [audit, clean-architecture, architecture, layers, backend]
---

# Clean Architecture Skill

Inspects backend code for **Clean Architecture** violations. Core rule: **dependencies point inward only**.

**Layers** (inner → outer): Entities (Domain) → Use Cases (Application) → Interface Adapters → Frameworks & Drivers

Each finding specifies: violation type, file path, severity (Critical/High/Medium/Low), evidence, remediation.

---

## Architectural Concerns

### 1 — The Dependency Rule

> *"Source code dependencies must only point inward."*

Inner layers never import from outer layers. Communication with outer layers uses abstractions (interfaces/protocols) defined in the inner layer.

**Look for:**
- Domain/entity importing `sqlalchemy`, `django.db`, `pymongo`, `redis`, `boto3`, `httpx`, ORM/framework modules
- Use-case importing concrete repository, FastAPI `Request`, Flask context, HTTP client
- Circular dependencies between layers
- Framework types in inner-layer function signatures

**Severity:**
- Domain imports ORM/framework: **Critical**
- Use-case instantiates concrete infrastructure: **High**
- Use-case accepts framework types (Request): **High**
- Circular dependency: **High**
- Minor utility import, no behavioral coupling: **Medium**

**Evidence:** File path, import statement, which layer → which layer, suggested fix (interface in inner layer, implementation in outer)

---

### 2 — Entity / Domain Layer Purity

> *"Entities encapsulate enterprise-wide business rules. They know nothing of persistence, transport, or frameworks."*

**Look for:**
- ORM base classes on entities (`db.Model`, `Base`, `Document`, `@Entity`)
- Serialization methods in entities (`to_json()`, `from_dict()`)
- Infrastructure imports in entity files
- Framework decorators on entity methods
- Entity methods that perform I/O (DB calls, HTTP, file writes)
- No distinct entity layer — entities ARE the ORM models

**Severity:**
- Entities are ORM models, no separation: **Critical**
- Entity methods perform I/O: **Critical**
- Entity imports infrastructure: **High**
- Entity has format-tied serialization: **Medium**
- Minor stdlib decorator: **Low**

**Evidence:** File path, ORM base/import/I/O call, suggested separation (pure entity + ORM model + mapper)

---

### 3 — Use Case / Application Layer Isolation

> *"Use cases orchestrate business logic. They know nothing about HTTP, CLI, databases, or message formats."*

**Look for:**
- Use cases importing framework modules (`fastapi`, `flask`, `django.http`)
- Use cases constructing HTTP responses, setting status codes
- Use cases directly accessing database (`session.query`, `collection.find`, raw SQL)
- Use cases handling transport concerns (headers, cookies, multipart uploads)
- Use cases with 5+ concrete infrastructure dependencies
- Use cases as pure pass-throughs with no logic
- Transaction management at infrastructure level (`session.commit`)

**Severity:**
- Use case imports/uses framework HTTP objects: **High**
- Use case constructs HTTP responses: **High**
- Use case calls ORM/DB without abstraction: **High**
- Use case manages transactions directly: **Medium**
- Use case is pure pass-through: **Medium**
- Minor utility dependency: **Low**

**Evidence:** File path, framework/infrastructure import, what belongs in another layer, suggested refactor

---

### 4 — Interface Adapters Layer (Controllers, Gateways, Presenters)

> *"Adapters translate between external formats and use-case inputs/outputs. They contain no business logic."*

**Look for:**
- Business logic in controllers/routers (validation, calculations, domain decisions)
- Fat controllers (>20-30 lines, more than parse → call use case → format output)
- Repository implementations with business rules (filtering by subscription status, age calculations)
- Missing adapter layer — controllers call entities directly
- Presenters/serializers that apply business logic
- Adapters that know about other adapters (controller references specific repository)

**Severity:**
- Route handlers contain substantial business logic (>10 lines): **High**
- Controllers bypass use-case layer, call domain directly: **High**
- Repository has business rules beyond data retrieval: **High**
- Controller instantiates concrete repository: **Medium**
- Use-case output leaked to HTTP with no mapping: **Medium**
- Minor formatting logic in controller: **Low**

**Evidence:** File path, business logic snippet, which layer it belongs to, suggested refactor

---

### 5 — Frameworks & Drivers Layer (Outermost)

> *"Frameworks and databases are details. The rest of the application should be unaware of specifics."*

**Look for:**
- Framework types/decorators/utilities used in every layer (not just outermost)
- Database config/connection in inner layers
- No separation — `app = FastAPI()` and routes mixed with use-case logic
- External service clients (`boto3`, `httpx`, `smtplib`) instantiated in inner layers
- Tests depend on live infrastructure

**Severity:**
- Framework types/decorators in domain/use-case: **High**
- Cannot unit-test logic without live infrastructure: **High**
- DB connection management in use-case: **Medium**
- Framework setup mixed with application logic: **Medium**
- External client instantiated in use case: **Medium**
- Minor framework utility in inner layer, no impact: **Low**

**Evidence:** File path, framework code/import, which layer, testability impact, suggested fix

---

### 6 — Boundary Contracts (Interfaces, Ports, Abstractions)

> *"At each boundary, interfaces define how inner layers communicate with outer layers."*

**Look for:**
- No interfaces/protocols/ABCs for external dependencies
- Interfaces defined in wrong layer (repository interface in infrastructure instead of domain/use-case)
- Interfaces expose infrastructure details (methods accept/return `Session`, `QuerySet`, `Cursor`)
- Leaky abstractions (interface requires understanding connection pooling, pagination cursors)
- Missing output boundary (use cases return data with no DTO)
- Inconsistent contracts (some use abstractions, others bypass them)

**Severity:**
- No abstractions at any boundary: **Critical**
- Interface defined in infrastructure layer: **High**
- Interface exposes ORM/infrastructure types: **High**
- Partial adoption (some use abstractions, some don't): **Medium**
- Missing output port/DTO: **Medium**
- Minor leaky abstraction: **Low**

**Evidence:** Interface file path (or absence), where defined vs. where it should be, infrastructure types exposed, affected use cases, suggested fix

---

## Audit Instructions

1. **Identify layers** — examine folder structure to map modules to layers (domain/entities → application/use_cases → adapters/controllers → infrastructure/frameworks). If no clear layering exists, flag as high-severity and stop.
2. **For each concern (1-6)**, review files using "Look for" patterns above.
3. **Collect findings** with: concern type, file path, title, snippet, severity, remediation.
4. **Report only observable violations** — actual imports, calls, missing abstractions.
5. **Respect project conventions** (hexagonal, onion, ports-and-adapters variants).
6. **Classify conservatively** — when in doubt, choose lower severity.
