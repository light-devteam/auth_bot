import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
import uvicorn

from config import logger
from src.api import router
from src.bot import bot


class App:
    __instance = None
    __initiated = False

    def __new__(cls, *args: list, **kwargs: dict) -> None:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(
        self,
        host: str = '127.0.0.1',
        port: int = 8000,
        workers: int = 1,
    ) -> None:
        if App.__initiated:
            logger.warning('App already initated!')
            return
        self.__api = FastAPI(
            title='Auth Bot',
            docs_url='/swagger',
            lifespan=self.lifespan,
        )
        self.__api.include_router(router)
        self.__host = host
        self.__port = port
        self.__workers = workers
        App.__initiated = True

    def run(self) -> None:
        uvicorn.run(
            app=self.__api,
            host=self.__host,
            port=self.__port,
            workers=self.__workers,
            access_log=False,
        )

    @asynccontextmanager
    async def lifespan(self, api: FastAPI) -> AsyncGenerator[None, None]:
        bot_task = asyncio.create_task(bot.run())
        logger.info('App started')
        try:
            yield
        finally:
            bot_task.cancel()
            try:
                await bot_task
            except asyncio.CancelledError:
                ...
            logger.info('App finished')

    @property
    def api(self) -> FastAPI:
        return self.__api
