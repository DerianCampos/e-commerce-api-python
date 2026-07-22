# Alembic Migrations Guide

This guide covers how to apply, rollback, and manage database migrations for this project.

---

## Prerequisites

- Virtual environment activated: `source .venv/bin/activate`
- Database running (see `compose.yml`)
- Environment config in place (e.g., `config_local.yml` or `.env`)

---

## Migration Chain

```
None → 43a57a0d9e2c (initial schema)
          ↓
      a1b2c3d4e5f6 (add products table)
          ↓
      b7e8f9a0b1c2 (add bands, sizes, variants)
          ↓
      c4d5e6f7a8b9 (remove band slug and formed_year)  ← HEAD
```

---

## Common Commands

### Check current revision

```bash
alembic current
```

### View full migration history

```bash
alembic history --verbose
```

---

## Apply Migrations

### Apply all pending migrations (upgrade to latest)

```bash
alembic upgrade head
```

### Apply a specific revision

```bash
alembic upgrade <revision_id>
```

**Example:**

```bash
alembic upgrade a1b2c3d4e5f6
```

---

## Rollback (Downgrade)

### Roll back one step

```bash
alembic downgrade -1
```

### Roll back to a specific revision

```bash
alembic downgrade <revision_id>
```

**Example — roll back to initial schema:**

```bash
alembic downgrade 43a57a0d9e2c
```

### Roll back everything (drop all migrated tables)

```bash
alembic downgrade base
```

> ⚠️ `downgrade base` reverts all migrations. All migrated tables will be dropped. This is destructive — confirm you have a backup or are working in a local/dev environment.

---

## Full Reset (Wipe and Reapply)

Use this to completely reset the schema locally:

```bash
alembic downgrade base
alembic upgrade head
```

---

## Create a New Migration

### Auto-generate from model changes

```bash
alembic revision --autogenerate -m "describe your change here"
```

> Always review the generated file in `alembic/versions/` before applying. Auto-generate does not detect every change (e.g., check constraints, server defaults).

### Create an empty migration (manual)

```bash
alembic revision -m "describe your change here"
```

---

## Revision IDs Reference

| Revision ID    | Description                                  |
|----------------|----------------------------------------------|
| `43a57a0d9e2c` | Initial schema (`users`)                     |
| `a1b2c3d4e5f6` | Add products table                           |
| `b7e8f9a0b1c2` | Add bands, t-shirt sizes, product variants   |
| `c4d5e6f7a8b9` | Remove band `slug` and `formed_year` columns |
