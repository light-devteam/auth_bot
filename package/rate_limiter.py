from typing import Callable

from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


class RateLimiter:
    DEFAULT_LIMIT = '5/second'

    def __init__(self) -> None:
        self.__limiter = Limiter(key_func=get_remote_address)

    def add_api(self, api: FastAPI) -> None:
        api.state.limiter = self.__limiter
        api.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    def __call__(self) -> Limiter:
        return self.__limiter

    @property
    def limit(self) -> Callable:
        return self.__limiter.limit


limiter = RateLimiter()
