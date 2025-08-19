

from aiogram.filters.callback_data import CallbackData

class choose_type_question_CallbackFactory(CallbackData, prefix="tp_ques"):
    type_question: bool  #0 = text, 1 = option
