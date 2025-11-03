from aiogram.utils.auth_widget import check_integrity
from fastapi import Request, Response, status, HTTPException

from src.api.v1.signature.validate.router import router
from src.schemas import ValidateAuthDataRequest
from config import settings


@router.post(
    '/auth_data',
    summary='Validate telegram authData',
    response_description='Return HTTP Status 200 OK if authData is valid',
    responses={
        status.HTTP_401_UNAUTHORIZED: {},
        status.HTTP_429_TOO_MANY_REQUESTS: {},
    },
)
async def validate_auth_data_signature(
    request: Request,
    validate_request: ValidateAuthDataRequest,
    response: Response,
) -> None:
    try:
        is_auth_data_valid = check_integrity(
            token=settings.BOT_TOKEN.get_secret_value(),
            data=validate_request.model_dump(),
        )
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if is_auth_data_valid:
        response.status_code = status.HTTP_200_OK
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
