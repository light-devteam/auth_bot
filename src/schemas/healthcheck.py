from pydantic import BaseModel

from src.enums import HealthStatus


class HealthCheck(BaseModel):
    name: str
    status: HealthStatus = HealthStatus.HEALTHY

    def __bool__(self) -> bool:
        return self.status == HealthStatus.HEALTHY


class HealthReport(BaseModel):
    status: HealthStatus = HealthStatus.HEALTHY
    healthchecks: list[HealthCheck] = []
