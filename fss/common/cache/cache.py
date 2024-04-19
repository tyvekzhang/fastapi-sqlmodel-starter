"""Abstract base class for Cache"""

from abc import ABC, abstractmethod
from typing import Any

from fss.common.cache.redis_manager import RedisManager
from fss.common.config import configs


class Cache(ABC):
    @abstractmethod
    async def get(self, key: str) -> Any:
        """Retrieve a value by key from the cache."""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, timeout=None):
        """Set the value of a key in the cache with an optional timeout."""
        pass

    @abstractmethod
    async def delete(self, key: str):
        """Delete a key from the cache."""
        pass

    @abstractmethod
    async def exists(self, key: str):
        """Check if a key exists in the cache."""
        pass


async def get_cache_client() -> Cache:
    """
    Init redis client or page cache client
    :return:
    """

    from fss.common.cache.redis_cache import RedisCache

    redis_client = await RedisManager.get_instance()
    if configs.enable_redis:
        return RedisCache(redis_client)
    else:
        from fss.common.cache.page_cache import PageCache

        return PageCache()
