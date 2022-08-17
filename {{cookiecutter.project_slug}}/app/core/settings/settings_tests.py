from functools import lru_cache
from typing import Optional

from . import (
    Settings,
    Localization,
    RedisSettings,
    KafkaSettings,
    ServiceSettings,
    TestingSettingsPostgres,
)


class TestingLocalization(Localization):
    LOCALE_DIR: str = "./app/locales"


class ProjectSettingsTesting(ServiceSettings):
    """Хранилище настроек для testing окружения."""

    localization = TestingLocalization()
    postgres: TestingSettingsPostgres = TestingSettingsPostgres()
    base_settings: Settings = Settings()
    redis: RedisSettings = RedisSettings()
    kafka: KafkaSettings = KafkaSettings()

    SENTRY_URL: Optional[str] = None
    ELASTIC_APM: Optional[dict] = None
    LOGGING_SERIALIZE: bool = False


@lru_cache
def get_settings(**kwargs):
    return ProjectSettingsTesting(**kwargs)
