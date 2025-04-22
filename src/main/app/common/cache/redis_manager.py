"""RedisManager to get redis instance"""

import asyncio
from typing import Optional

import redis.asyncio as redis

from src.main.app.common.config.config_manager import load_config


class RedisManager:
    _instance: Optional[redis.Redis] = None
    _connection_pool: Optional[redis.ConnectionPool] = None
    _lock = asyncio.Lock()

    @classmethod
    async def get_instance(cls) -> redis.Redis:
        """
        Get redis instance
        """
        if cls._instance is None:
            async with cls._lock:
                if cls._connection_pool is None:
                    database = load_config().database
                    cls._connection_pool = redis.ConnectionPool.from_url(
                        f"redis://:{database.cache_pass}@{database.cache_host}:{database.cache_port}/{database.db_num}",
                        decode_responses=True,
                    )
                if cls._instance is None:
                    cls._instance = await redis.Redis.from_pool(cls._connection_pool)
        return cls._instance
