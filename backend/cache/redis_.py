from datetime import timedelta, datetime, date
from typing import Any, Generator

from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio.client import Pipeline, Redis

from backend.config.redis import REDIS_CONFIG, RedisConfig


class RedisTool:
    def __init__(self, redis_config: RedisConfig = REDIS_CONFIG):
        self.connection: Redis = aioredis.from_url(**redis_config.get_redis_attributes(redis_config.api_db_index))
        self.pipe: Pipeline | None = None

    async def connect_fastapi_cache(self):
        FastAPICache.init(RedisBackend(self.connection), prefix='fastapi-cache')

    async def disconnect(self):
        await self.connection.close()

    async def get_keys(self) -> list[Any]:
        return [key for key in await self.connection.keys(pattern='*')]

    async def get_value(self, key: str) -> str | None:
        return await self.connection.get(key)

    async def set_item(self, key: str, value: bytes | str, expires: int | timedelta | datetime | date = None):
        connection = self.pipe if self.pipe is not None else self.connection

        await connection.set(key, value)
        if isinstance(expires, timedelta) or isinstance(expires, int):
            await connection.expire(key, expires)
        if isinstance(expires, datetime):
            await connection.expire(key, expires - datetime.utcnow())

    async def delete_item(self, key: str):
        connection = self.pipe if self.pipe is not None else self.connection

        await connection.delete(key)

    async def delete_all_values(self):
        connection = self.pipe if self.pipe is not None else self.connection

        keys = await connection.keys('*')
        await connection.delete(*keys)


class RedisContextManager:
    def __init__(self, redis_config: RedisConfig = REDIS_CONFIG):
        self.redis_config = redis_config

    async def __aenter__(self) -> RedisTool:
        self.redis = RedisTool(self.redis_config)
        return self.redis

    async def __aexit__(self, exc_type, exc, tb):
        await self.redis.disconnect()


async def get_redis_session() -> Generator[RedisTool, None, None]:
    async with RedisContextManager() as redis:
        async with redis.connection.pipeline(transaction=True) as pipe:
            redis.pipe = pipe
            yield redis
            await redis.pipe.execute()
