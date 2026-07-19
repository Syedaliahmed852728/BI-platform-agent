from __future__ import annotations

from functools import lru_cache

import redis
import redis.asyncio as aioredis

from configs.data import data_settings


@lru_cache(maxsize=1)
def get_sync_redis() -> redis.Redis:
    return redis.from_url(data_settings.redis_url, decode_responses=False)


@lru_cache(maxsize=1)
def get_async_redis() -> aioredis.Redis:
    return aioredis.from_url(data_settings.redis_url, decode_responses=True)
