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


class ProjectSettingsLocal(ServiceSettings):
    """Хранилище настроек для dev окружения."""

    localization = Localization()
    postgres: BaseSettingsPostgres = BaseSettingsPostgres()
    redis: RedisSettings = RedisSettings()
    kafka: KafkaSettings = KafkaSettings()
    base_settings: Settings = Settings()

    SENTRY_URL: Optional[str] = None
    LOCAL_DOMAIN: str = "mastermind.svc.cluster.local"

    ELASTIC_APM: Optional[dict] = None


@lru_cache
def get_settings(**kwargs):
    return ProjectSettingsLocal(**kwargs)
