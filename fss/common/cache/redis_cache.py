"""Redis cache implementation"""

import asyncio
from typing import Optional

import redis.asyncio as redis

from fss.common.cache.cache import Cache
from fss.common.config import configs


class RedisManager:
    _instance: Optional[redis.Redis] = None
    _connection_pool: Optional[redis.ConnectionPool] = None
    _lock = asyncio.Lock()

    @classmethod
    async def get_instance(cls) -> redis.Redis:
        """

        :return:
        """
        if cls._instance is None:
            async with cls._lock:
                if cls._connection_pool is None:
                    cls._connection_pool = redis.ConnectionPool.from_url(
                        f"redis://:{configs.cache_pass}@{configs.cache_host}:{configs.cache_port}"
                    )
                if cls._instance is None:
                    cls._instance = await redis.Redis.from_pool(cls._connection_pool)
        return cls._instance


class RedisCache(Cache):
    def __init__(self, redis_client):
        self.redis_client = redis_client

    async def get(self, key):
        """Retrieve a value by key from Redis."""
        return await self.redis_client.get(key)

    async def set(self, key, value, timeout=None):
        """Set the value of a key in Redis with an configsal timeout."""
        if timeout:
            await self.redis_client.setex(key, timeout, value)
        else:
            await self.redis_client.set(key, value)

    async def delete(self, key):
        """Delete a key from Redis."""
        return await self.redis_client.delete(key)

    async def exists(self, key):
        """Check if a key exists in Redis."""
        return await self.redis_client.exists(key)
