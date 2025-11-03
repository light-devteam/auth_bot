from src.api.v1.healthcheck.router import router
from src.api.v1.healthcheck.liveness import router
from src.api.v1.healthcheck.readiness import router

__all__ = [
    'router',
]
