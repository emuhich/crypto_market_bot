from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from handlers.users.tools import get_button_next_back
from keyboards.inline.callback_datas import faq_callback, get_question_callback
from keyboards.inline.dynamic_faq import faq_keyboard, back_to_faq
from loader import dp
from utils.db_api.db_commands import select_all_questions, get_question


@dp.callback_query_handler(faq_callback.filter(command_name="show_faq"))
async def show_faq(call: CallbackQuery, callback_data: dict):
    questions = await select_all_questions()
    start = int(callback_data.get("start"))
    end = int(callback_data.get("end"))
    next, back = await get_button_next_back(len(questions), end, start)
    questions = questions[start:end]
    await call.message.edit_text(text="\n".join(
        [
            f'❔ {hbold(f"Часто задаваыемые вопросы")}\n',
            f'Выберете вопрос который вас инетерсует.',
            f'Если такого вопроса нет вы можете всегда обратится в поддержку',

        ]
    ), reply_markup=faq_keyboard(start, end, next, back, questions))


@dp.callback_query_handler(get_question_callback.filter(command_name="get_question"))
async def back_to_profile(call: CallbackQuery, callback_data: dict):
    pk = int(callback_data.get("pk"))
    start = int(callback_data.get("start"))
    end = int(callback_data.get("end"))
    question = await get_question(pk)
    await call.message.edit_text(text="\n".join(
        [
            f'❔ {hbold(question.questions)}❔\n ',
            question.answer,

        ]
    ), reply_markup=back_to_faq(start, end))
