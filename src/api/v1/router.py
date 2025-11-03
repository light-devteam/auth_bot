from fastapi import APIRouter

from src.api.v1.healthcheck import router as healthcheck_router
from src.api.v1.signature import router as signature_router


router = APIRouter(prefix='/v1')
router.include_router(healthcheck_router)
router.include_router(signature_router)
