from fastapi import APIRouter

from .check import router as check_router


API_VERSION = "v1"
router = APIRouter()

router.include_router(check_router, prefix='/check')
