import os
from typing import Optional
from redis.asyncio import Redis, ConnectionError

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client: Optional[Redis] = None

async def connect_redis() -> None:
    global redis_client
    if redis_client is None:
        redis_client = Redis.from_url(REDIS_URL, decode_responses=True, socket_timeout=2)
        try:
            await redis_client.ping()
        except ConnectionError:
            # leave client object but ping failed; callers should handle exceptions
            pass

async def close_redis() -> None:
    global redis_client
    if redis_client is not None:
        await redis_client.close()
        redis_client = None

def get_redis() -> Redis:
    if redis_client is None:
        raise RuntimeError("Redis client not connected; ensure connect_redis was run on startup")
    return redis_client
