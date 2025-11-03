from fastapi import Request, status

from src.api.v1.healthcheck.router import router
from src.schemas import HealthReport
from package import limiter


@router.get(
    '/live',
    summary='Perform a Liveness Health Check',
    response_description='Return HTTP Status Code 200 (OK)',
    responses={
        status.HTTP_429_TOO_MANY_REQUESTS: {},
    },
)
@limiter.limit(limiter.DEFAULT_LIMIT)
async def healthcheck_liveness(request: Request) -> HealthReport:
    return HealthReport()
