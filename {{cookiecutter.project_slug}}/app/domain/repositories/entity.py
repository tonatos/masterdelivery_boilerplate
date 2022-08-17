import abc
import json
from typing import Optional, List, Union

from sqlalchemy import select

from core.settings import settings
from core.base.repository import BaseRepository
from ..models import Entity
from ..schemas.redis.entity import EntityRedisSchema


class EntityRepository(BaseRepository):
    @abc.abstractmethod
    async def get(self, id: int):
        pass

    @abc.abstractmethod
    async def list(self):
        pass

    @abc.abstractmethod
    async def save(self, entity):
        pass


class EntityDBRepository(EntityRepository):
    async def get(self, id: int) -> Union[None, Entity]:
        res = await self.db.execute(
            select(Entity).where(Entity.id == id)
        )
        return res.scalars().first()

    async def list(self) -> List[Entity]:
        res = await self.db.execute(select(Entity))
        return res.scalars().all()

    async def save(self, entity: Entity) -> Entity:
        self.db.add(entity)
        return entity


class EntityCachedRepository(EntityDBRepository):
    key = f'{settings.base_settings.PROJECT_NAME}:entity'

    async def get(self, id: int) -> Optional[EntityRedisSchema]:
        try:
            return EntityRedisSchema(**json.loads(await self.redis.get(f"{self.key}:{id}")))
        except TypeError:
            return None

    async def list(self) -> List[EntityRedisSchema]:
        return [
            EntityRedisSchema(**json.loads(j))
            for j in await self.redis.mget(
                keys=await self.redis.keys(f'{self.key}:*')
            )
        ]

    async def save(self, entity: EntityRedisSchema) -> EntityRedisSchema:
        await self.redis.set(f"{self.key}:{entity.id}", value=entity.json())
        return entity
