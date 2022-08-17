import uuid
import random
from typing import List, Optional

from fastapi import APIRouter, Depends

from mm_authentication import get_current_user, User, UserRoleEnum

from domain.interactors.entity.entity_command import EntityCommandInteractor
from .response.entity import EntityResponse

router = APIRouter()


@router.get("/")
async def base_response():
    return {"message": "That`s ok!"}


@router.get(
    "/permitted/",
    summary="Check route for permitted request with token",
)
async def permitted_route(
    iam: User = Depends(
        get_current_user(
            UserRoleEnum.ADMIN,
            UserRoleEnum.SUPERVISOR,
            UserRoleEnum.COURIER,
            UserRoleEnum.MERCHANT
        )
    ),
):
    return {"message": f"Hello {iam.user_id}!"}


@router.get(
    "/kafka/",
    summary="Check kafka work",
)
async def check_kafka(name: str):
    return {"message": f"Kafka ok!"}


@router.get(
    "/redis/",
    response_model=List[EntityResponse],
    summary="Check redis connection and redis work",
)
async def check_redis(
    entity_id: Optional[uuid.UUID] = None,
    command_interactor: EntityCommandInteractor = Depends(EntityCommandInteractor)
):
    return await command_interactor.check_redis_work(
        id=entity_id if entity_id else uuid.uuid1(),
        value=str(random.random())
    )


@router.get(
    "/db/",
    response_model=List[EntityResponse],
    summary="Check db connection and db work"
)
async def check_db(
    entity_id: Optional[uuid.UUID] = None,
    command_interactor: EntityCommandInteractor = Depends(EntityCommandInteractor)
):
    return await command_interactor.check_db_work(
        id=entity_id if entity_id else uuid.uuid1(),
        value=str(random.random())
    )
