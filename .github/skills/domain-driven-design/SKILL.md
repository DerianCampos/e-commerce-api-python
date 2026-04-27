---
name: domain-driven-design
description: 'Code review skill for Domain-Driven Design (DDD). Use when auditing a codebase for DDD compliance: Entities, Value Objects, Aggregates, Aggregate Roots, Repositories, Domain Services, Application Services, Bounded Contexts, Domain Events, Ubiquitous Language, anti-corruption layers, tactical and strategic patterns. Produces classified findings with severity ratings and remediation guidance.'
version: 1.0.0
tags: [audit, domain-driven-design, ddd, architecture, backend]
---

# Domain-Driven Design Skill

Inspects a codebase for **DDD** violations — tactical (entity/aggregate/repository/service) and strategic (bounded contexts, ubiquitous language, anti-corruption layers). Business rules belong in the domain model; never in controllers, repositories, or infrastructure.

Each finding: category code · file path · severity (Critical/High/Medium/Low) · evidence · remediation.

**Categories:** `AGG` Aggregate · `ENT` Entity · `VO` Value Object · `REPO` Repository · `DSVC` Domain Service · `ASVC` Application Service · `DE` Domain Event · `BC` Bounded Context · `UL` Ubiquitous Language · `ACL` Anti-Corruption Layer · `INF` Infrastructure Leak · `ADM` Anemic Domain Model

---

## DDD Concerns

### 1 — Ubiquitous Language
> *"Code and domain model must share a single, consistent language from domain experts."*

**Look for:** Names drifting from domain vocabulary · technical names (`Manager`, `Helper`, `Handler`) where domain terms belong · same concept named differently across files (synonym sprawl) · DB column or DTO names leaking into domain model naming.

**Severity:** Pervasive technical naming: **High** · synonym sprawl: **Medium** · isolated name drift: **Low**

**Evidence:** File path, offending name(s), correct domain term, breadth of drift

---

### 2 — Entities
> *"An entity has stable identity across state changes. Equality is identity, not value."*

**Look for:** No explicit stable ID · equality done property-by-property · public setters bypassing domain methods · invariant validation scattered outside the entity.

**Severity:** No identity concept: **Critical** · public setters on core entities / invariants enforced externally: **High** · individual setter on non-critical property: **Medium** · missing identity-based `equals`/`__eq__`: **Low**

**Evidence:** File path, setter or missing-ID location, externalized invariants, suggested domain methods

---

### 3 — Value Objects
> *"A value object is defined by its attributes. It is immutable and has no identity."*

**Look for:** Setters or mutable state · equality by reference instead of all-component values · primitives used where a VO would enforce invariants (primitive obsession) · VO carrying an ID or DB key.

**Severity:** Mutable VO / pervasive primitive obsession: **High** · missing value-based equality on core VO: **Medium** · single minor primitive obsession: **Low**

**Evidence:** File path, mutable property or missing equality, unprotected invariant, suggested VO

---

### 4 — Aggregates & Aggregate Roots
> *"An aggregate is a consistency boundary. Only the root is referenced from outside. Cross-aggregate refs use IDs only."*

**Look for:** No identifiable aggregate root · external code referencing inner members directly · object references to other aggregates instead of IDs · god aggregates (>5 unrelated entities) · trivially small aggregates · invariants enforced outside the root.

**Severity:** No aggregate boundaries: **Critical** · external mutation of internals / cross-aggregate object refs: **High** · god aggregate / invariant in application service: **Medium** · aggregate too small but harmless: **Low**

**Evidence:** File path, bypassed member or cross-ref, unprotected invariant, suggested boundary

---

### 5 — Repositories
> *"One repository per aggregate root. Interface in domain; implementation in infrastructure."*

**Look for:** Multiple repo interfaces per aggregate · interface defined in infrastructure layer · returns DTO/raw ORM object/lazy-load proxy instead of reconstructed domain object · query methods using ORM/SQL vocabulary · ORM imports in domain or application layer.

**Severity:** Interface in infrastructure or missing / returns ORM object / ORM imports in domain layer: **High** · infrastructure vocabulary in query methods / multiple repos per aggregate: **Medium**

**Evidence:** File path, interface location vs. correct layer, leaking return type or import, suggested fix

---

### 6 — Domain Services
> *"A domain service models operations that belong to no single entity and involve only domain logic."*

**Look for:** Stateful domain services · infrastructure dependencies (HTTP, DB, messaging) · logic that naturally belongs on an entity/VO placed in a service (anemic-model enabler) · invoked directly from controllers.

**Severity:** Direct infrastructure calls / offloading logic from anemic entities: **High** · stateful service / invoked from controller: **Medium**

**Evidence:** File path, infrastructure import or displaced logic, missing domain concept, suggested refactor

---

### 7 — Application Services / Use-Cases
> *"Application services orchestrate the domain. They contain no business rules."*

**Look for:** Business rules or domain decisions inside application services · depends on concrete repos instead of interfaces · cross-cutting concerns (transactions, auth, logging) bleeding into the domain layer · bypasses domain model with direct DB calls.

**Severity:** All logic in app services, domain model empty: **Critical** · significant domain logic in app service / depends on concrete infra: **High** · cross-cutting concern in domain layer: **Medium** · minor orchestration shortcut: **Low**

**Evidence:** File path, logic snippet that belongs in domain, which aggregate/entity should own it, suggested refactor

---

### 8 — Domain Events
> *"Domain events capture what happened. Raised inside aggregates; handled outside."*

**Look for:** Significant state changes with no domain event · events named in present tense or non-domain vocabulary · events raised outside the aggregate · mutable events · handlers inside the domain layer.

**Severity:** No events in state-change-heavy domain / raised outside aggregate / handlers in domain layer: **High** · present-tense naming / mutable events: **Medium** · isolated missing event for minor change: **Low**

**Evidence:** File path, state change or publish call location, handler layer, naming example, suggested fix

---

### 9 — Bounded Contexts
> *"A bounded context is an explicit boundary. Contexts communicate through contracts, not shared classes."*

**Look for:** No identifiable context boundaries · contexts sharing domain model classes directly · same concept forced into one model across contexts with legitimately different views · bidirectional or implicit inter-context dependencies.

**Severity:** No boundaries in a multi-domain system / shared domain classes: **High** · bidirectional coupling / forced unified model: **Medium**

**Evidence:** File path(s), cross-boundary classes/modules, which context should own what, suggested separation

---

### 10 — Anti-Corruption Layer (ACL)
> *"Translate at the boundary. Never let external models infect the domain."*

**Look for:** External system types (third-party models, legacy DTOs) used inside domain classes · no translation layer for external integrations · translation logic scattered instead of centralized.

**Severity:** External types inside domain entities/aggregates / no ACL for complex integration: **High** · scattered translation logic: **Medium**

**Evidence:** File path, external type used, polluted domain concept, suggested ACL location

---

### 11 — Infrastructure Leaks
> *"ORM annotations, DB types, and framework base classes belong in infrastructure — not in domain entities."*

**Look for:** ORM annotations/attributes (`@Column`, `@Table`, `[Key]`) on domain entities · framework base classes (`db.Model`, `@Entity`) inherited by entities · DB session/connection management outside infrastructure · HTTP/messaging imports in domain or application layer.

**Severity:** Domain entities extend ORM base or carry annotations: **Critical** · HTTP/messaging imports in domain / DB session in application layer: **High** · single ORM annotation on otherwise clean entity: **Medium**

**Evidence:** File path, import/annotation/base class, infrastructure concern it represents, suggested separation

---

### 12 — Anemic Domain Model
> *"Domain objects must have behavior, not just data. Logic scattered in services is an anti-pattern."*

**Look for:** Entities/aggregates as pure data bags (only getters/setters, no domain methods) · substantial business logic in application services, controllers, or scripts that belongs in the domain · domain objects used as DTOs between layers.

**Severity:** Entire domain layer is data-only, all logic in services: **Critical** · core aggregates with no domain methods: **High** · individual entity missing behavior for key operation: **Medium** · minor missing behavior on peripheral entity: **Low**

**Evidence:** File path(s), service/controller logic that belongs in domain, which entity should own it, suggested domain methods

---

## Audit Instructions

1. **Identify structure** — map folders to DDD layers (domain, application, infrastructure). If no domain layer exists, flag Critical (`ADM`) before continuing.
2. **For each concern (1–12)**, review relevant files using the "Look for" patterns.
3. **Collect findings** with: category code, file path, title, evidence snippet, severity, remediation.
4. **Report only observable violations** — actual imports, class definitions, method bodies. No speculative findings.
5. **Respect conventions** — adjust for CQRS, hexagonal, or other variants the team uses.
6. **Classify conservatively** — when in doubt, choose the lower severity.
