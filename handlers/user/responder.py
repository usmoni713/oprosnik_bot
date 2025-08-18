from keyboards import buttons

from aiogram.types import CallbackQuery, Message



async def send_meny(message:Message):

    await message.answer("нажмите на кнопку чтобы помотреть актывние опросы", 
    reply_markup=await buttons.creat_bt_list_quiz())