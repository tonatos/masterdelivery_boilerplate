import sentry_sdk
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from mm_healthchecker import add_health_router
from mm_i18n import I18nMiddleware, load_translations
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from core.errors.http_error import http_error_handler
from core.errors.validation_error import http422_error_handler
from core.settings import settings
from core.events import create_start_app_handler, create_stop_app_handler
from core.logging import app_logger
from api import router as api_router


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.base_settings.PROJECT_NAME,
        debug=settings.base_settings.DEBUG,
        version=settings.base_settings.VERSION,
        openapi_url=f"{settings.base_settings.API_PREFIX}/v1/{settings.base_settings.PROJECT_NAME}/openapi.json",  # noqa
    )
    logger = app_logger
    application.logger = logger

    load_translations(
        domain=settings.localization.GETTEXT_DOMAIN,
        accept_languages=settings.localization.ACCEPT_LANGUAGES,
        default_language=settings.localization.DEFAULT_LANGUAGE,
        localedir=settings.localization.LOCALE_DIR,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.base_settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    application.add_middleware(
        I18nMiddleware,
        default_language=settings.localization.DEFAULT_LANGUAGE,
        accept_languages=settings.localization.ACCEPT_LANGUAGES,
    )

    application.add_event_handler('startup', create_start_app_handler(application))
    application.add_event_handler('shutdown', create_stop_app_handler(application))

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application = add_health_router(application, settings.base_settings.PROJECT_NAME)
    application.include_router(api_router, prefix=settings.base_settings.API_PREFIX)

    return application


app = get_application()

if settings.SENTRY_URL:
    sentry_sdk.init(
        settings.SENTRY_URL,
        traces_sample_rate=0.1,
        release=settings.CI_COMMIT_SHORT_SHA,
        environment=settings.SENTRY_ENV,
    )
    app.add_middleware(SentryAsgiMiddleware)
