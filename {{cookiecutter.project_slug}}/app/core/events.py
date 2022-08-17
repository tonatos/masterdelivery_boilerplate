from typing import Callable

import mm_tracing
from fastapi import FastAPI

from core.settings import settings
from .connections.db import connect_to_db, close_db_connection
from .connections.redis import connect_to_redis, close_redis_connection
from .connections.kafka import connect_to_kafka, close_kafka_connection


def create_start_app_handler(app: FastAPI) -> Callable:
    """Подключение зависимостей для приложения.

    Args:
        app: Экземпляр приложения
    """

    async def start_app() -> None:
        if settings.ELASTIC_APM:
            mm_tracing.init(app.title, fastapi=app, raw_config=settings.ELASTIC_APM)
        await connect_to_db(app)
        await connect_to_redis(app)
        await connect_to_kafka(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    """Отключение зависимостей для приложения.

    Args:
        app: Экземпляр приложения
    """

    async def stop_app() -> None:
        await close_db_connection(app)
        await close_redis_connection(app)
        await close_kafka_connection(app)

    return stop_app
