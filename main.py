
import asyncio
from email import message
from re import T
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from handlers.user import user_handlars

TOKEN = "6516484967:AAEzhT_ZOBazXaFaNF5M0gKumQXZxub0gOk"

dp = Dispatcher()


async def run():
    bot = Bot(TOKEN)
    dp.include_router(user_handlars.user_router)
    await dp.start_polling(bot)

asyncio.run(run())