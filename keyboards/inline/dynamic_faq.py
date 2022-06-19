from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import SUPPORT_LINK
from keyboards.inline.callback_datas import faq_callback, get_question_callback


def faq_keyboard(start, end, next, back, questions):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for question in questions:
        question_button = InlineKeyboardButton(text=question.questions,
                                               callback_data=get_question_callback.new(command_name="get_question",
                                                                                       pk=question.pk,
                                                                                       start=start,
                                                                                       end=end
                                                                                       ))
        keyboard.row(question_button)

    back_button = InlineKeyboardButton(text="← Пред", callback_data=faq_callback.new(command_name="show_faq",
                                                                                     start=start - 8,
                                                                                     end=end - 8
                                                                                     ))
    next_button = InlineKeyboardButton(text="След →", callback_data=faq_callback.new(command_name="show_faq",
                                                                                     start=start + 8,
                                                                                     end=end + 8
                                                                                     ))
    if next and back:
        keyboard.row(back_button, next_button)
    elif next and back is False:
        keyboard.row(next_button)
    elif back and next is False:
        keyboard.row(back_button)
    button_support_link = InlineKeyboardButton(text="👨🏻‍💻 Поддержка", url=SUPPORT_LINK)
    back_button = InlineKeyboardButton(text="⬅️ Назад", callback_data="menu")
    keyboard.row(back_button, button_support_link)
    return keyboard


def back_to_faq(start, end):
    keyboard = InlineKeyboardMarkup(row_width=1)
    FAQ_start_button = InlineKeyboardButton(text="⬅️ Назад", callback_data=faq_callback.new(
        command_name="show_faq",
        start=start,
        end=end
    ))
    keyboard.insert(FAQ_start_button)
    return keyboard
