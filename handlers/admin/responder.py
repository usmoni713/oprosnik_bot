
from keyboards import admin_buttons

from aiogram.types import Message

async def send_admin_panel(message:Message):
    await message.answer("Админ-меню:", reply_markup=await admin_buttons.creat_admin_panel(message))

async def get_type_question(message:Message, curent_question:int):
    await message.answer(f"Укажите тип вопроса({curent_question}):", 
    reply_markup=await admin_buttons.creat_buttons_for_choose_type_question(message))