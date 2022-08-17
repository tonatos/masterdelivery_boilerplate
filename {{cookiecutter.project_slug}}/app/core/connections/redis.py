from fastapi import FastAPI
from databases import DatabaseURL
from redis import asyncio as aioredis

from ..settings import settings


def _connect_via_sentinel(db_url) -> aioredis.Redis:
    sentinel = aioredis.Sentinel(
        [(db_url.hostname, db_url.port)],
        db=settings.redis.REDIS_DB,
        password=settings.redis.REDIS_PASS,
        socket_timeout=settings.redis.REDIS_TIMEOUT,
        max_connections=settings.redis.REDIS_POOL_MAX,
    )
    return sentinel.master_for(settings.redis.REDIS_CLUSTER_NAME)


def _connect_via_pool(db_url) -> aioredis.Redis:
    pool = aioredis.ConnectionPool(
        host=db_url.hostname,
        port=db_url.port,
        db=settings.redis.REDIS_DB,
        password=settings.redis.REDIS_PASS,
        max_connections=settings.redis.REDIS_POOL_MAX,
        socket_timeout=settings.redis.REDIS_TIMEOUT
    )
    return aioredis.Redis(connection_pool=pool)


async def connect_to_redis(app: FastAPI) -> None:
    db_url = DatabaseURL(settings.redis.REDIS_HOST)

    app.state.redis = _connect_via_sentinel(db_url) \
        if settings.redis.REDIS_CLUSTER_NAME \
        else _connect_via_pool(db_url)


async def close_redis_connection(app: FastAPI) -> None:
    await app.state.redis.close()
