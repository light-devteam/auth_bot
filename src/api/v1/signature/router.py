from fastapi import APIRouter

from src.api.v1.signature.validate import router as validate_router


router = APIRouter(
    prefix='/signature',
    tags=['Signature'],
)
router.include_router(validate_router)
