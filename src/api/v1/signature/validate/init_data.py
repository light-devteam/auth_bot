from aiogram.utils.web_app import check_webapp_signature
from fastapi import Request, status, Response, HTTPException

from src.api.v1.signature.validate.router import router
from src.schemas import ValidateInitDataRequest
from config import settings


@router.post(
    '/init_data',
    summary='Validate telegram initData',
    response_description='Return HTTP Status 200 OK if initData is valid',
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_429_TOO_MANY_REQUESTS: {},
    },
)
async def validate_init_data_signature(
    request: Request,
    validate_request: ValidateInitDataRequest,
    response: Response,
) -> None:
    is_valid = check_webapp_signature(
        token=settings.BOT_TOKEN.get_secret_value(),
        init_data=validate_request.init_data.get_secret_value(),
    )
    if is_valid:
        response.status_code = status.HTTP_200_OK
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
