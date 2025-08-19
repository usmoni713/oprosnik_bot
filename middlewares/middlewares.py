from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from config import admins_id
class CheckUserForAdmin(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: Dict[str, Any]) -> Any:
        user: User = data.get("event_from_user")
        if user_id in admins_id:
            user.bot.send_message(user.id, f"YOU ARE ADMIN\nusrid= {user.id}")
            result = await handler(event, data)
            return result
        else: 
            user.bot.send_message(user.id, f"YOU ARE NOT ADMIN!!!!\nusrid= {user.id}")
            return
