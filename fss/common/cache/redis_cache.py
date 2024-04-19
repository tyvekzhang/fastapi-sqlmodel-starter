"""Redis cache implementation"""

from typing import Any

from fss.common.cache.cache import Cache


class RedisCache(Cache):
    def __init__(self, redis_client):
        self.redis_client = redis_client

    async def get(self, key: str) -> Any:
        """Retrieve a value by key from Redis."""
        return await self.redis_client.get(key)

    async def set(self, key: str, value: Any, timeout=None):
        """Set the value of a key in Redis with timeout."""
        if timeout:
            await self.redis_client.setex(key, timeout, value)
        else:
            await self.redis_client.set(key, value)

    async def delete(self, key: str):
        """Delete a key from Redis."""
        return await self.redis_client.delete(key)

    async def exists(self, key: str):
        """Check if a key exists in Redis."""
        return await self.redis_client.exists(key)
