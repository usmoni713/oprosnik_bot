from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from filters import ferma_callbacks as fc

async def creat_admin_panel(message:Message):
    builder = ReplyKeyboardBuilder()
    builder.button(text="Создать новый опрос")
    builder.button(text="Управление опросами")
    builder.button(text="Выгрузить результаты")
    builder.button(text="Рассылка опроса")
    builder.adjust(1)
    return builder.as_markup()
    
async def creat_buttons_for_choose_type_question(message:Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="текст", callback_data=fc.choose_type_question_CallbackFactory(type_question=False)) 
    builder.button(text="варианты", callback_data=fc.choose_type_question_CallbackFactory(type_question=True))
    builder.adjust(2)
    return builder.as_markup()