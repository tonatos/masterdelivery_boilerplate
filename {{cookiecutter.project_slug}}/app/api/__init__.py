from fastapi import APIRouter

import api.v1 as api_v1
from core.settings import settings


router = APIRouter()

router.include_router(
    api_v1.router,
    tags=[f"public_{api_v1.API_VERSION}_router"],
    prefix=f"/{api_v1.API_VERSION}/{settings.base_settings.PROJECT_NAME}",
)
