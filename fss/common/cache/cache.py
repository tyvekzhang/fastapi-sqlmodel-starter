"""Abstract base class for Cache"""

from abc import ABC, abstractmethod


from fss.common.config import configs


class Cache(ABC):
    @abstractmethod
    async def get(self, key):
        """Retrieve a value by key from the cache."""
        pass

    @abstractmethod
    async def set(self, key, value, timeout=None):
        """Set the value of a key in the cache with an optional timeout."""
        pass

    @abstractmethod
    async def delete(self, key):
        """Delete a key from the cache."""
        pass

    @abstractmethod
    async def exists(self, key):
        """Check if a key exists in the cache."""
        pass


async def get_cache_client() -> Cache:
    """
    Init redis client or page cache client
    :return:
    """
    if configs.enable_redis:
        from fss.common.cache.redis_cache import RedisCache
        from fss.common.cache.redis_cache import RedisManager

        redis_client = await RedisManager.get_instance()
        return RedisCache(redis_client)
    from fss.common.cache.page_cache import PageCache

    return PageCache()
