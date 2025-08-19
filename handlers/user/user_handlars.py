from handlers.user import responder as rs

from aiogram import Router, F
from aiogram.types import Message, user
import asyncio
from aiogram.filters import BaseFilter


from config import admins_id
user_router = Router()

class IsNotdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user is not None and message.from_user.id in admins_id

user_router.message.filter(IsNotdmin())
user_router.callback_query.filter(IsNotdmin())



@user_router.message(F.text=="/start")
async def start_comand(message:Message):
    # await message.answer("привет! это бот опросник.")
    await rs.send_meny(message=message)

