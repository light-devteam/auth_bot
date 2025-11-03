from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.exceptions import TelegramRetryAfter

from src.bot.handlers.router import router
from src.bot.templates import render


async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    start_message = await message.answer(text=render('start'))
    try:
        await message.bot.unpin_all_chat_messages(message.chat.id)
    except TelegramRetryAfter:
        ...
    await start_message.pin()


@router.message(CommandStart())
async def start_message(message: Message, state: FSMContext) -> None:
    await start(message, state)
