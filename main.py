
import asyncio
from email import message
from re import T
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from handlers.user import user_handlars
from handlers.admin import admin_handler
from config import TOKEN


dp = Dispatcher()


async def run():
    print("Start polling")
    bot = Bot(TOKEN)
    
    dp.include_router(admin_handler.admin_router)
    
    dp.include_router(user_handlars.user_router)

    await dp.start_polling(bot)

asyncio.run(run())