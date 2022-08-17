import os
from functools import lru_cache
from typing import List, Optional

from databases import DatabaseURL
from pydantic import BaseSettings, validator

from .. import BASE_DIR


class ServiceSettings(BaseSettings):
    """Базовый класс для настроек проекта."""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class ENVSettings(ServiceSettings):
    ENV: str = "prod"
    STAGES_WITH_CONSUL: List[str] = ["prod", "stage"]

    def is_production(self):
        return self.ENV in self.STAGES_WITH_CONSUL

    def is_testing(self):
        return self.ENV == "testing"


class BaseSettingsPostgres(ServiceSettings):
    """Настройки для postgresql."""

    PG_USER: str
    PG_PASS: str
    PG_HOST: str
    PG_PORT: Optional[int] = 5432
    PG_DB_NAME: str
    MIN_CONNECTIONS_COUNT: int = 10
    MAX_CONNECTIONS_COUNT: int = 10
    DATABASE_URL: DatabaseURL = None
    DB_ECHO: bool = True
    DB_USE_CONNECTION_FOR_REQUEST: bool = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DATABASE_URL = DatabaseURL(
            "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(
                self.PG_USER,
                self.PG_PASS,
                self.PG_HOST,
                self.PG_PORT,
                self.PG_DB_NAME,
            )
        )


class TestingSettingsPostgres(ServiceSettings):
    """Настройки для postgresql."""

    TESTING_PG_USER: str
    TESTING_PG_PASS: str
    TESTING_PG_HOST: str
    TESTING_PG_PORT: Optional[int] = 5432
    TESTING_PG_DB_NAME: str
    MIN_CONNECTIONS_COUNT: int = 10
    MAX_CONNECTIONS_COUNT: int = 10
    DATABASE_URL: DatabaseURL = None
    DB_ECHO: bool = True
    DB_USE_CONNECTION_FOR_REQUEST: bool = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DATABASE_URL = DatabaseURL(
            "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(
                self.TESTING_PG_USER,
                self.TESTING_PG_PASS,
                self.TESTING_PG_HOST,
                self.TESTING_PG_PORT,
                self.TESTING_PG_DB_NAME,
            )
        )

    def __getattr__(self, name):
        if name.startswith("PG_"):
            if getattr(self, f"TESTING_{name}"):
                return getattr(self, f"TESTING_{name}")
            else:
                raise AttributeError


class RedisSettings(ServiceSettings):
    REDIS_HOST: str = 'redis://0.0.0.0:6379'
    REDIS_PASS: Optional[str]
    REDIS_DB: int = 0
    REDIS_POOL_MIN: int = 0
    REDIS_POOL_MAX: int = 10
    REDIS_TIMEOUT: int = 10
    REDIS_CLUSTER_NAME: Optional[str]


class KafkaSettings(ServiceSettings):
    KAFKA_PRODUCE_TOPIC: str = ''
    KAFKA_CONSUME_TOPIC: str = ''
    KAFKA_BROKERS: str = ''
    KAFKA_USERNAME: str = ''
    KAFKA_PASSWORD: str = ''
    KAFKA_SECURITY_PROTOCOL: str = 'SASL_PLAINTEXT'
    KAFKA_SASL_MECHANISM: str = ''


class Localization(ServiceSettings):
    """Настройки для локализации и интернационализации."""

    REGION: str = "RU"
    GETTEXT_DOMAIN: str = "base"
    DEFAULT_LANGUAGE: str = "ru" if REGION.lower() == "ru" else "en"
    ACCEPT_LANGUAGES: str = "de,en,es,fr,it,ru,tr"
    LOCALE_DIR: str = os.path.join(BASE_DIR, "app/locales")

    @validator("ACCEPT_LANGUAGES")
    def perform_accept_languages_to_list(cls, v: str) -> List[str]:
        return v.split(",")


class Settings(ServiceSettings):
    API_PREFIX: str = "/api"
    PRIVATE_PREFIX: str = "/private"
    VERSION: str = "0.0.0"

    ALLOWED_HOSTS: str = 'http://localhost:3000'
    DEBUG: bool = False
    PROJECT_NAME: str = "{{ cookiecutter.project_slug }}"

    # Logger
    LOGGING_SERIALIZE: bool = True
    LOGGING_LEVEL: str = "debug"

    # Sentry
    CI_COMMIT_SHORT_SHA: str = "local"

    @validator("ALLOWED_HOSTS")
    def perform_allowed_hosts_to_list(cls, v: str) -> List[str]:
        return v.replace(" ", "").split(",")


@lru_cache
def get_env_settings(**kwargs):
    return ENVSettings(**kwargs)


if get_env_settings().is_production():
    from .settings_prod import get_settings
elif get_env_settings().is_testing():
    from .settings_tests import get_settings
else:
    from .settings_local import get_settings

settings = get_settings()
