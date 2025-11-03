import asyncio

from fastapi import Request, Response, status

from src.api.v1.healthcheck.router import router
from src.schemas import HealthReport
from src.enums import HealthStatus
from package import limiter


@router.get(
    '/ready',
    summary='Perform a Readiness Health Check',
    response_description='Checks the status of all service dependencies',
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {},
        status.HTTP_429_TOO_MANY_REQUESTS: {},
    },
    response_model=HealthReport,
)
@limiter.limit(limiter.DEFAULT_LIMIT)
async def healthcheck_readiness(request: Request, response: Response) -> HealthReport:
    healthcheckers = []
    healthchecks = await asyncio.gather(*healthcheckers)
    if all(healthchecks):
        health_status = HealthStatus.HEALTHY
        response.status_code = status.HTTP_200_OK
    else:
        health_status = HealthStatus.UNHEALTHY
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return HealthReport(
        status=health_status,
        healthchecks=healthchecks,
    )
