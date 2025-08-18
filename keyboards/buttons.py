import asyncio


from aiogram.utils.keyboard import ReplyKeyboardBuilder

async def creat_bt_list_quiz():
    build = ReplyKeyboardBuilder()
    build.button(text="доступные опросы")
    return build.as_markup()
