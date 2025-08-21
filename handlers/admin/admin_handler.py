from gc import callbacks
from multiprocessing import current_process
from pyexpat.errors import messages
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, message_entity
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext

from handlers.admin import responder as rs
from handlers.admin.states import creat_new_quiz
from filters import ferma_callbacks as fc

from config import admins_id
from database import setup_db as database
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
    await state.update_data(questions=[])

    await state.set_state(creat_new_quiz.add_question.choice_type_question)
    await rs.get_type_question(message, 1)


@admin_router.callback_query(fc.choose_type_question_CallbackFactory.filter(), creat_new_quiz.add_question.choice_type_question)
async def creat_new_quiz_etap3(callback:CallbackQuery, callback_data:fc.choose_type_question_CallbackFactory, state:FSMContext):
    await state.update_data(type_question=callback_data.type_question)
    await state.set_state(creat_new_quiz.add_question.enter_text_question)

    await callback.message.answer(f"Вводите текст вопроса({(await state.get_data()).get("corent_question")}):")


async def check_if_this_last_question_if_yes_add_to_db(message:Message,data:dict)->bool:
    if data.get("corent_question") >= data.get("quantity_of_questions"):
            db = database.Database()
            await db.add_new_quiz(
                name_quiz=data.get('name_quiz'),
                status=0,
                quantity_of_questions=data.get('quantity_of_questions'),
                questions_=data.get("questions")
            )

            await message.answer(text=f"опрос {data.get('name_quiz')} успешно создан")
            return True
    else: return False
async def receive_next_question(message:Message, state:FSMContext, corent_question:int):
    await rs.get_type_question(message, corent_question +1)
    await state.update_data(corent_question=corent_question +1)
    await state.set_state(creat_new_quiz.add_question.choice_type_question)
        

@admin_router.message(creat_new_quiz.add_question.enter_text_question)
async def creat_new_quiz_etap4(message:Message, state:FSMContext):
    await state.update_data(text_question=message.text)
    data = await state.get_data()
    if data.get("type_question"):
        # print(f'{data.get("type_question")=}')
        await message.answer("Вводите варианты ответов через запятую")
        await state.set_state(creat_new_quiz.add_question.enter_options_for_question)
    else:
        
        corent_question = data.get('corent_question')
        questions:list = data.get("questions")
        questions.append(
            {"type_question":"text", 
            "text_question":message.text,
            }
        )
        await state.update_data(questions=questions)
        await message.answer(f"{corent_question} вопрос успешно добавлен!")
        
        check_if_this_last_question= await check_if_this_last_question_if_yes_add_to_db(message, data)
        if check_if_this_last_question:
            await state.clear()
            return
        
        
        await receive_next_question(message, state, corent_question)
        
#TODO нужно добавить проверку введёныые данные на соответстие с ожидаемым типом даннных 
@admin_router.message(creat_new_quiz.add_question.enter_options_for_question)
async def creat_new_quiz_etap5(
    message:Message,
    state:FSMContext
):
    data = await state.get_data()
    options = [message.text.split(',')]
    for i in options:
        print(i)
    questions:list = data.get("questions")
    questions.append(
            {"type_question":"option", 
            "text_question":data.get("text_question"),
            "options_for_question":options
            }
    )
    await state.update_data(questions= questions)
    data = await state.get_data()

    check_if_this_last_question = await check_if_this_last_question_if_yes_add_to_db(message, data)
    if check_if_this_last_question:
        await state.clear()
        return
    await receive_next_question(message, state, data.get("corent_question"))





