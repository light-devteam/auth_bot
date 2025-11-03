from aiogram import Bot as AiogramBot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeAllPrivateChats
from aiogram.types import BotCommand

from config import settings, logger
from src.exceptions import GWAlreadyInitiatedException
from src.bot.handlers import router
from src.bot.middlewares import ThrottlingMiddleware


class Bot:
    __DEFAULT_BOT_PROPERTIES = DefaultBotProperties(parse_mode=ParseMode.HTML)
    __COMMANDS = (
        BotCommand(command='start', description='Перезапустить бота'),
    )
    __instance = None
    __initiated = False

    def __new__(cls, *args: list | tuple, **kwargs: dict) -> 'Bot':
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(
        self,
        dispatcher: Dispatcher | None = None,
        bot: AiogramBot | None = None,
    ) -> None:
        if Bot.__initiated:
            logger.warning('Bot already initiated!')
            raise GWAlreadyInitiatedException()
        if dispatcher is None:
            dispatcher = Dispatcher(storage=None)
            self.__setup_dispatcher(dispatcher)
        if bot is None:
            bot = AiogramBot(token=settings.BOT_TOKEN.get_secret_value(), default=self.__DEFAULT_BOT_PROPERTIES)
        self._dispatcher = dispatcher
        self._bot = bot
        self.__is_setuped = False
        Bot.__initiated = True

    def __setup_dispatcher(self, dispatcher: Dispatcher) -> None:
        dispatcher.include_router(router)
        dispatcher.message.outer_middleware(ThrottlingMiddleware(limit=2))

    async def setup(self) -> None:
        if self.__is_setuped:
            logger.debug('Bot already setuped!')
            return
        await self._bot.delete_webhook()
        await self._bot.set_my_commands(
            commands=self.__COMMANDS,
            scope=BotCommandScopeAllPrivateChats(),
        )
        self.__is_setuped = True
        logger.debug('Bot successfully setuped!')

    async def run(self) -> None:
        if not self.__is_setuped:
            await self.setup()
        logger.info('Bot started!')
        await self._dispatcher.start_polling(self._bot, handle_signals=False)
        logger.info('Bot stopped!')

    @property
    def dispatcher(self) -> Dispatcher:
        return self._dispatcher

    @property
    def bot(self) -> AiogramBot:
        return self._bot


bot = Bot()
