import os
import json
import asyncio
from typing import Any, Awaitable, Callable, Optional
from redis.exceptions import RedisError
from ..redis_client import get_redis

ENV = os.getenv("ENV", "dev")
CACHE_VERSION = os.getenv("CACHE_VERSION", "v1")

def _key(product_id: int) -> str:
    return f"myshop:{ENV}:product:{product_id}:{CACHE_VERSION}"

async def get_product(
    product_id: int,
    loader_fn: Callable[[int], Awaitable[Optional[dict]]],
    ttl_seconds: int = 300
) -> Optional[dict]:
    key = _key(product_id)
    try:
        r = get_redis()
        raw = await r.get(key)
        if raw is not None:
            return json.loads(raw)
    except (RedisError, RuntimeError):
        pass

    lock_key = f"{key}:lock"
    got_lock = False
    try:
        r = get_redis()
        got_lock = await r.set(lock_key, "1", nx=True, ex=5)
    except (RedisError, RuntimeError):
        got_lock = False

    if not got_lock:
        await asyncio.sleep(0.05)
        try:
            r = get_redis()
            raw = await r.get(key)
            if raw is not None:
                return json.loads(raw)
        except (RedisError, RuntimeError):
            pass

    product = await loader_fn(product_id)

    try:
        r = get_redis()
        if product is None:
            await r.set(key, json.dumps(None), ex=30)
        else:
            await r.set(key, json.dumps(product), ex=ttl_seconds)
    except (RedisError, RuntimeError):
        pass
    finally:
        if got_lock:
            try:
                r = get_redis()
                await r.delete(lock_key)
            except Exception:
                pass

    return product

async def invalidate_product(product_id: int) -> None:
    try:
        r = get_redis()
        await r.delete(_key(product_id))
    except Exception:
        pass
