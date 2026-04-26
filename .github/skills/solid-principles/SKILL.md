---
name: solid-principles
description: Audits for SOLID violations (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion).
version: 1.0.0
tags: [audit, solid, oop, code-quality, backend]
---

# SOLID Principles Skill

Inspects backend code for **SOLID** violations — five OO design principles for maintainable, extensible, testable code.

Each finding specifies: principle, file path, severity, evidence, remediation.

---

## The Five SOLID Principles

---

### S — Single Responsibility Principle (SRP)

> *"A class (or module, function) should have one, and only one, reason to change."*

One unit = one cohesive concern. If it changes for multiple unrelated reasons (business rules AND persistence), it has >1 responsibility.

**Look for:**
- God classes/functions handling unrelated concerns (validation + email + DB + API responses)
- Method count bloat (>15-20 methods spanning unrelated operations)
- Mixed abstraction levels (high-level orchestration + low-level I/O in one function)
- Multiple import groups (persistence + email + external APIs + validation)
- Unrelated reasons to change (changes when email provider changes AND when DB schema changes)
- Test complexity (mocking 5+ unrelated dependencies)

**Severity:**
- Core domain class handles persistence + business logic + presentation: **High**
- Service class manages infrastructure concerns (sends emails, writes files): **High**
- Utility function handles 3+ unrelated transformations: **Medium**
- Minor method doing slightly more than name implies: **Low**

**Evidence:** File path, class/function, distinct responsibilities list, key methods grouped by responsibility, imports

---

### O — Open/Closed Principle (OCP)

> *"Software entities should be open for extension, but closed for modification."*

Add new behavior by writing new code, not editing existing tested code.

**Look for:**
- Large `if/elif/else` or `switch` on type tags (`if entity_type == "invoice": ... elif entity_type == "order": ...`)
- `isinstance` chains (multiple checks to dispatch behavior by concrete type)
- Hard-coded strategy selection (instantiates specific implementations based on conditions vs. accepting abstraction)
- Frequent modification of core class for new features (git history shows edits every sprint)
- No ABCs/protocols/interfaces where behavior varies by type

**Severity:**
- Core processing logic uses long type-dispatch chain growing with features: **High**
- Class modified for every new payment method/report type/notification channel: **High**
- Minor conditional for new edge case in clean class: **Low**
- Missing abstraction reducing future modification risk: **Medium**

**Evidence:** File path, function/class, conditional chain/`isinstance` block, what new behavior requires, suggested abstraction

---

### L — Liskov Substitution Principle (LSP)

> *"Objects of a subclass should be substitutable for objects of their superclass without altering correctness."*

If `B extends A`, you must use `B` wherever `A` is expected with correct behavior. Subclass weakening preconditions, strengthening postconditions, or raising unexpected exceptions breaks substitution.

**Look for:**
- Overridden methods throwing `NotImplementedError` or `raise NotImplemented`
- Overridden methods doing nothing (`pass`)
- Subclass requiring more restrictive inputs than parent
- Subclass returning narrower/incompatible type than parent's declared return
- Subclass changing meaning of inherited behavior (parent's `save()` persists; subclass also sends notification)
- ABCs with methods concrete subclasses only partially implement
- Type narrowing in overrides (`isinstance` inside overridden method)

**Severity:**
- Subclass raises `NotImplementedError` for widely-used inherited method: **Critical**
- Subclass silently ignores critical parent behavior (no-op `save()`): **High**
- Subclass changes return type incompatibly: **High**
- Subclass adds unexpected side effect not in parent: **Medium**
- Minor behavioral inconsistency with minimal impact: **Low**

**Evidence:** Parent/subclass file paths, overridden method(s), parent contract vs. subclass delivery, callers at risk

---

### I — Interface Segregation Principle (ISP)

> *"Clients should not be forced to depend on methods they do not use."*

Small focused interfaces over large ones. Classes shouldn't implement methods irrelevant to their purpose.

**Look for:**
- Fat ABCs (>6-8 abstract methods) concrete implementations only partially use
- `pass` or `raise NotImplementedError` in concrete implementations (forced to satisfy irrelevant contract)
- Forced imports of unused interface methods
- Single interface serving very different client types (e.g., `Repository` with read-only AND write-only methods)
- Overly generic base classes (`BaseProcessor` with `process()`, `validate()`, `serialize()`, `notify()`, `persist()`)
- Concrete classes stubbing half an inherited interface

**Severity:**
- Fat interface forces all implementors to stub methods → silent no-ops at runtime: **High**
- Large ABC with many unused abstract methods in most implementations: **High**
- Interface slightly broader than needed, no runtime impact: **Medium**
- Minor method on interface one implementation doesn't need: **Low**

**Evidence:** Base class/interface file path, methods defined vs. implemented (stubs highlighted), concrete classes affected, proposed split

---

### D — Dependency Inversion Principle (DIP)

> *"High-level modules should not depend on low-level modules. Both should depend on abstractions."*

Business logic (high-level) must not be directly wired to infrastructure (low-level): databases, email, filesystems, HTTP, queues. Both depend on abstraction (interface/protocol/ABC); concrete implementation injected.

**Look for:**
- Direct instantiation of infrastructure inside business logic (`self.db = PostgreSQLConnection(...)`, `self.mailer = SendGridClient(...)`)
- Hard-coded concrete infrastructure imports in domain/service (`from infrastructure.postgres import UserRepository`)
- No dependency injection (services create own dependencies vs. receiving via constructor/args/DI framework)
- Untestable without real infrastructure (can't test by passing mock/fake)
- `os`, `subprocess`, `smtp`, `boto3`, `httpx` calls directly in domain logic
- No repository/gateway/adapter patterns (direct ORM/SQL/HTTP in service/use-case)
- Config/secrets read directly (`os.environ["DB_URL"]` in domain class)

**Severity:**
- Core business logic directly instantiates/calls DB or external API (untestable without live infrastructure): **Critical**
- Service imports concrete repository directly, no abstraction: **High**
- Domain function reads env vars/config directly: **High**
- Low-level utility in one minor helper, no wider impact: **Low**
- Missing abstraction improving testability, no current runtime risk: **Medium**

**Evidence:** File path, class/method, import/instantiation snippet, test exists? (how handled?), suggested abstraction

---

## Audit Instructions

1. **Traverse source tree** — classes, modules, functions in domain, service, application, infrastructure layers. Skip auto-generated, migrations, test fixtures.
2. **For each principle (S, O, L, I, D)**, review files using "Look for" patterns.
3. **Collect findings** with: principle, file path, class/function, title, snippet, severity, remediation.
4. **Report only observable violations** — backed by code patterns.
5. **Classify conservatively** — when in doubt, choose lower severity.
