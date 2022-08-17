from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from fastapi import FastAPI

from ..settings import settings


async def connect_to_db(app: FastAPI) -> None:
    app.state.pool = create_async_engine(
        str(settings.postgres.DATABASE_URL),
        connect_args={
            "prepared_statement_cache_size": 0
        },
        pool_size=settings.postgres.MIN_CONNECTIONS_COUNT,
        max_overflow=(
            settings.postgres.MAX_CONNECTIONS_COUNT - settings.postgres.MIN_CONNECTIONS_COUNT
        ),
        echo=settings.postgres.DB_ECHO
    )

    app.state.session = sessionmaker(
        app.state.pool,
        class_=AsyncSession,
        expire_on_commit=False
    )


async def close_db_connection(app: FastAPI) -> None:
    await app.state.pool.dispose()
