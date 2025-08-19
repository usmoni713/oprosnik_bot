from keyboards import user_buttons 

from aiogram.types import CallbackQuery, Message



async def send_meny(message:Message):

    await message.answer(f"нажмите на кнопку чтобы помотреть актывние опросы\n usrid = {message.from_user.id}", 
    reply_markup=await user_buttons.creat_bt_list_quiz())