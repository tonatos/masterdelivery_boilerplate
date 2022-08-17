import abc
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(
        self,
        db: AsyncSession,
        redis: Redis
    ) -> None:
        self._db = db
        self._redis = redis
        self._cache_place = {}

    @property
    def redis(self) -> Redis:
        return self._redis

    @property
    def db(self) -> AsyncSession:
        return self._db
