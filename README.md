# FastAPI + Redis + Async SQLAlchemy cache-aside example

This PR adds an async Redis cache-aside example to the FastAPI app and includes a minimal async SQLAlchemy setup and Alembic configuration.

Quick start (dev):
1. Start Postgres and Redis: docker-compose up -d
2. Install deps: pip install -r requirements.txt
3. Set DATABASE_URL and REDIS_URL env vars if different from defaults.
4. Run Alembic migrations: alembic upgrade head
5. Run app: uvicorn app.main:app --reload

Notes:
- The PR includes a Product model, async DB session dependency, and cache helpers.
- Cache keys use CACHE_VERSION env var for easy invalidation when payload shape changes.
- For production use a managed Redis service, TLS, AUTH, and proper monitoring.
