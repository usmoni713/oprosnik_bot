from handlers.user import responder as rs

from aiogram import Router, F
from aiogram.types import Message
import asyncio

user_router = Router()

@user_router.message(F.text=="/start")
async def start_comand(message:Message):
    # await message.answer("привет! это бот опросник.")
    await rs.send_meny(message=message)

