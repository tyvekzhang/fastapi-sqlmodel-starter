"""Simple in-memory page cache implementation"""

from typing import Any

import diskcache

from fss.common.cache.cache import Cache


class PageCache(Cache):
    def __init__(self):
        self.cache = diskcache.Cache()

    async def get(self, key: str) -> Any:
        """Retrieve a value by key from the in-memory cache."""
        return self.cache.get(key)

    async def set(self, key: str, value: Any, timeout: int = None) -> None:
        """Set the value for a key in the in-memory cache."""
        self.cache.set(key, value)
        if timeout:
            self.cache.expire(key, timeout)

    async def delete(self, key: str) -> bool:
        """Delete a key from the in-memory cache."""
        if key in self.cache:
            self.cache.delete(key)
            return True
        return False

    async def exists(self, key: str) -> bool:
        """Check if a key exists in the in-memory cache."""
        if key in self.cache:
            return True
        return False
