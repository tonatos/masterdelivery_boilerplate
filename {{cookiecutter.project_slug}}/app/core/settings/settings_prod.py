from functools import lru_cache
from typing import Optional

from . import (
    BaseSettingsPostgres,
    Localization,
    ServiceSettings,
    RedisSettings,
    KafkaSettings,
    Settings,
)


def get_base_settings() -> dict:
    return {
        'ENV': 'prod',
        'DOMAIN': 'localhost',
        'REGION': 'ru',
    }


def get_sentry_url(service_name: str) -> str:
    return service_name


def get_elastic_url() -> str:
    return 'elastic'


def get_postgres_settings(service_name: str) -> dict:
    return {
        "PG_HOST": 'host',
        "PG_PORT": 5432,
        "PG_DB_NAME": service_name,
        "PG_USER": 'user',
        "PG_PASS": 'password',
    }


class ProjectSettingsProduction(ServiceSettings):
    """Хранилище настроек для prod окружения."""
    data = get_base_settings()

    SERVICE_NAME: str = Settings().PROJECT_NAME
    SENTRY_URL: Optional[str] = get_sentry_url(SERVICE_NAME)
    LOCAL_DOMAIN: str = data["DOMAIN"]
    ENV: str = data["ENV"]

    localization = Localization(REGION=data["REGION"])
    postgres: BaseSettingsPostgres = BaseSettingsPostgres(
        **get_postgres_settings(SERVICE_NAME)
    )
    redis: RedisSettings = RedisSettings()
    kafka: KafkaSettings = KafkaSettings()
    base_settings: Settings = Settings()

    ELASTIC_APM: Optional[dict] = get_elastic_url()


@lru_cache
def get_settings():
    return ProjectSettingsProduction()
