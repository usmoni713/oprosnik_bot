from aiogram.fsm.state import State, StatesGroup

class creat_new_quiz(StatesGroup):
    name_quiz = State()
    quantity_of_questions = State()
    class add_question(StatesGroup):
        choice_type_question = State()
        enter_text_question = State()
        enter_options_for_question = State()
