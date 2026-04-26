---
name: dry-kiss-yagni
description: Audits for DRY (Don't Repeat Yourself), KISS (Keep It Simple), and YAGNI (You Aren't Gonna Need It) violations — duplication, unnecessary complexity, speculative features.
version: 1.0.0
tags: [audit, dry, kiss, yagni, code-quality, backend]
---

# DRY, KISS & YAGNI Principles Skill

Detects waste, complexity, and duplication violations.

| Principle | Question |
|---|---|
| **DRY** | "Is the same knowledge expressed in more than one place?" |
| **KISS** | "Is this more complex than it needs to be?" |
| **YAGNI** | "Does this code serve a current requirement, or a hypothetical future one?" |

Each finding specifies: principle, file path, severity, evidence, remediation.

---

## The Three Principles

---

### DRY — Don't Repeat Yourself

> *"Every piece of knowledge must have a single, unambiguous, authoritative representation."*

**Not** just duplicate lines — duplicate **knowledge**, **business logic**, or **decisions**. When one concept lives in multiple places, changes require updating every copy.

**Look for:**
- Copy-pasted blocks (≥5 lines, only variable name changes)
- Business rules in 2+ locations (discount formula in OrderService AND InvoiceService)
- Parallel data structures manually kept in sync (UserDTO, UserResponse, UserPayload with same fields)
- Magic values hard-coded in multiple files (timeouts, thresholds, regex)
- Duplicated query logic in separate repositories
- Repeated error handling patterns (same try/except across endpoints)
- Duplicated validation rules (same checks in multiple places)

**NOT a violation:** Code that looks similar but expresses **different knowledge** — merging creates accidental coupling.

**Severity:**
- Business rule duplicated across 3+ files: **Critical**
- Large copy-paste (≥20 lines) in 2+ files: **High**
- Magic value hard-coded in multiple files: **High**
- Same query logic in 2 places: **Medium**
- Same validation in 2 places with minor differences: **Medium**
- Small repeated pattern (3-5 lines) twice: **Low**

**Evidence:** File paths, line ranges, side-by-side comparison, knowledge duplicated, # locations, de-duplication strategy

---

### KISS — Keep It Simple, Stupid

> *"Everything should be made as simple as possible, but not simpler."*

Code should match problem complexity — no simpler, no more complex. Violations introduce unnecessary layers, indirections, or abstractions adding cognitive load without benefit.

**Look for:**
- Premature abstraction (factories, strategies for single implementation, no second planned)
- Deep inheritance (>3 levels) where flat composition/functions would work
- Unnecessary design patterns (GoF patterns where simple if/else would be clearer)
- Excessive indirection (4+ layer call chain with pure pass-throughs)
- Clever/cryptic code (nested comprehensions, chained ternaries requiring comments to explain *what*)
- Over-parameterized functions (6+ parameters, multiple boolean flags, **kwargs catch-alls)
- Unnecessary generics/metaclasses/decorator stacks with no use case
- Convoluted control flow (>3 nesting levels, mixed early returns with nested try/except)
- Abstraction layers with no behavior (just forward calls)

**NOT a violation:** Complexity **inherent to the problem domain** — KISS targets **accidental** complexity.

**Severity:**
- Entire architectural layer serving one use case, no extension plan: **High**
- Deep inheritance (>3 levels) creating coupling, composition simpler: **High**
- Factory/builder/strategy wrapping single implementation: **Medium**
- Function with 8+ parameters or 3+ boolean flags: **Medium**
- Cryptic one-liner, hard to understand but localized: **Low**
- Unnecessary wrapper with no added logic: **Low**

**Evidence:** File path, complex construct snippet, why more complex than needed, simpler alternative, does it serve current requirement

---

### YAGNI — You Aren't Gonna Need It

> *"Implement things when you actually need them, never when you foresee you might need them."*

Code for **speculative future requirements** is a liability: must be read, tested, maintained — for a scenario that may never arrive or differ from what was imagined.

**Look for:**
- Unused code (classes, functions, methods, endpoints, modules never called/imported/referenced)
- Commented-out code with intent comments (`# TODO: enable when we add multi-tenancy`)
- Unused feature flags/config (keys, env vars, toggles defined but never read)
- Speculative parameters (defaults never overridden anywhere)
- Pre-built extension points with no consumers (abstract methods, hooks, callbacks with one implementation, no external use)
- Over-designed data models (DB columns, fields defined but never read/written)
- Premature optimization (caching, bulk processing, connection tuning before performance problem)
- Unused dependencies (libraries in requirements not imported)
- Speculative abstractions ("in case we swap implementations" — only one exists, no plan for another)

**NOT a violation:** Code required by **current sprint/feature/task** or team architecture guidelines.

**Severity:**
- Entire module/service for non-existent feature, not on roadmap: **High**
- Unused public API endpoints (potential security surface): **High**
- Unused DB columns/tables adding migration complexity: **Medium**
- Unused dependencies (CVE exposure): **Medium**
- Speculative parameter never overridden: **Low**
- Small commented TODO for nebulous future: **Low**
- One unused private helper: **Low**

**Evidence:** File path, unused code name, evidence of no usage (no references/imports), speculative intent, maintenance cost, suggested action

---

## Audit Instructions

1. **Traverse source tree** — source code, config files, dependency manifests, data models. Skip auto-generated files, migrations, lock files, test fixtures.
2. **For each principle**, review files using "Look for" patterns.
3. **Collect findings** with: principle, file path, title, snippet, severity, remediation.
4. **Report only observable violations** — confirmed duplication (same knowledge), confirmed simpler alternative, confirmed unused code.
5. **Distinguish DRY from accidental similarity** — only flag when repeated code encodes **same knowledge**.
6. **Distinguish KISS from essential complexity** — only flag **accidental** complexity.
7. **Classify conservatively** — when in doubt, choose lower severity.
