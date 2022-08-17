from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type

from starlette.requests import Request

from ..base.repository import BaseRepository


class Repository:
    @property
    def _get_session(self) -> AsyncSession:
        return self.request.app.state.session

    @property
    def _get_redis_pool(self) -> Redis:
        return self.request.app.state.redis

    async def _get_session_from_pool(self) -> AsyncSession:
        async with self._get_session() as session:
            yield session

    def __init__(self, repo_type: Type[BaseRepository]):
        self.repo_type = repo_type

    async def __call__(self, request: Request) -> BaseRepository:
        self.request = request

        async def _get_repo() -> BaseRepository:
            db_session = await self._get_session_from_pool().__anext__()
            return self.repo_type(
                db=db_session,
                redis=self._get_redis_pool
            )

        return await _get_repo()
