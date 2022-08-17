from typing import List
from enum import Enum
from functools import wraps
from sqlalchemy.ext.asyncio import AsyncSession

from ..base.repository import BaseRepository

session = None


class Propagation(Enum):
    REQUIRED = "required"
    REQUIRED_NEW = "required_new"


class Transactional:
    def _get_session(self, function) -> AsyncSession:
        params = inspect.signature(function).parameters
        for o in args:
            for param in o.__dict__.values():
                if isinstance(param, BaseRepository):
                    return param.db

    def __init__(self, propagation: Propagation = Propagation.REQUIRED):
        self.propagation = propagation

    def __call__(self, function):
        @wraps(function)
        async def decorator(*args, **kwargs):
            self.sessions = self._get_session(args=args)

            try:
                if self.propagation == Propagation.REQUIRED:
                    result = await self._run_required(
                        function=function,
                        args=args,
                        kwargs=kwargs,
                    )
                elif self.propagation == Propagation.REQUIRED_NEW:
                    result = await self._run_required_new(
                        function=function,
                        args=args,
                        kwargs=kwargs,
                    )
                else:
                    result = await self._run_required(
                        function=function,
                        args=args,
                        kwargs=kwargs,
                    )
            except Exception as e:
                await self.session.rollback()
                raise e

            return result

        return decorator

    async def _run_required(self, function, args, kwargs) -> None:
        result = await function(*args, **kwargs)
        await self.session.commit()
        return result

    async def _run_required_new(self, function, args, kwargs) -> None:
        self.session.begin()
        result = await function(*args, **kwargs)
        await self.session.commit()
        return result

