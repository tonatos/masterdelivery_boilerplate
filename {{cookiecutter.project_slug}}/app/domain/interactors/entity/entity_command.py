import uuid
from uuid import UUID
from typing import NoReturn, Union, Type, List
from fastapi import Depends

from core.utils.transactional import Transactional, Propagation
from core.base.repository import BaseRepository
from core.dependencies.repository import Repository
from core.exceptions.base import BadRequestException
from ...repositories.entity import EntityCachedRepository, EntityDBRepository
from ...schemas.redis.entity import EntityRedisSchema
from ...schemas.db.entity import EntityDBSchema
from ...models import Entity


class EntityCommandInteractor:
    @Transactional(propagation=Propagation.REQUIRED)
    async def check_db_work(
            self,
            id: UUID = None,
            value: str = None,
            entity_db_repo: Type[BaseRepository] = Depends(
                Repository(EntityDBRepository)
            ),
    ) -> Union[NoReturn, List[EntityDBSchema]]:
        if not value:
            raise BadRequestException

        entity = await entity_db_repo.get(id=id)
        if entity:
            entity.value = value
            return [EntityDBSchema.from_orm(
                await entity_db_repo.save(entity=entity)
            )]

        entity = Entity.create(
            value=str(value)
        )
        await entity_db_repo.save(entity=entity)
        return [EntityDBSchema.from_orm(e) for e in await entity_db_repo.list()]

    async def check_redis_work(
            self,
            id: UUID,
            value: str,
            entity_redis_repo: Type[BaseRepository] = Depends(
                Repository(EntityCachedRepository)
            ),
    ) -> Union[NoReturn, List[EntityRedisSchema]]:
        entity = await entity_redis_repo.get(id=id)
        if entity:
            entity.value = value
            return [await entity_redis_repo.save(entity=entity)]

        await entity_redis_repo.save(
            entity=EntityRedisSchema(**{'id': id, 'value': value})
        )
        return await entity_redis_repo.list()
