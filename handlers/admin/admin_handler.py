from gc import callbacks
from multiprocessing import current_process
from pyexpat.errors import messages
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext

from handlers.admin import responder as rs
from handlers.admin.states import creat_new_quiz
from filters import ferma_callbacks as fc

from config import admins_id
admin_router = Router(name="admin_router")

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user is not None and message.from_user.id in admins_id


admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())



@admin_router.message(F.text=="/start")
async def start_command(message:Message):
    await message.answer("you are admin!\n /admin")

@admin_router.message(F.text == "/admin")
async def admin_command(message:Message):
    await  rs.send_admin_panel(message)

@admin_router.message(F.text == "Создать новый опрос")
async def creat_new_quiz_etap1(message:Message, state:FSMContext):
    await state.set_state(creat_new_quiz.name_quiz)
    await message.answer("вводите название опроса:")

@admin_router.message(creat_new_quiz.name_quiz)
async def creat_new_quiz_etap2(message:Message, state:FSMContext):
    # await state.update_data()
    await state.update_data(name_quiz=message.text)
    await state.set_state(creat_new_quiz.quantity_of_questions)
    await message.answer("вводите количества вопросов в опросе(от 1 до 20):")


@admin_router.message(creat_new_quiz.quantity_of_questions)
async def creat_new_quiz_etap2(message:Message, state:FSMContext):
    
    
    await state.update_data(quantity_of_questions=int(message.text))
    await state.update_data(corent_question=1)

    await state.set_state(creat_new_quiz.add_question.choice_type_question)
    await rs.get_type_question(message, 1)


@admin_router.callback_query(fc.choose_type_question_CallbackFactory.filter(), creat_new_quiz.add_question.choice_type_question)
async def creat_new_quiz_etap3(callback:CallbackQuery, callback_data:fc.choose_type_question_CallbackFactory, state:FSMContext):
    await state.update_data(type_question=callback_data.type_question)
    await state.set_state(creat_new_quiz.add_question.enter_text_question)

    await callback.message.answer("Вводите текст вопроса:")

@admin_router.message(creat_new_quiz.add_question.enter_text_question)
async def creat_new_quiz_etap4(message:Message, state:FSMContext):
    await state.update_data(text_question=message.text)
    data = await state.get_data()
    if data.get("type_question"):
        print(f'{data.get("type_question")=}')
        # ...
    else:
        # TODO добавить вопрос в бд
        corent_question = data.get('corent_question')
        await message.answer(f"{corent_question} вопрос успешно добавлен!")
        if corent_question >= data.get("quantity_of_questions"):
            await message.answer(text=f"опрос {data.get('name_quiz')} успешно создан")
            await state.clear()
            return
        await rs.get_type_question(message, corent_question +1)
        await state.update_data(corent_question=corent_question +1)
        await state.set_state(creat_new_quiz.add_question.choice_type_question)
        
#TODO нужно добавить проверку введёныые данные на соответстие с ожидаемым типом даннных 





    



    

