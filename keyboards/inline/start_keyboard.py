from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import SUPPORT_LINK
from keyboards.inline.callback_datas import faq_callback

start_keyboard = InlineKeyboardMarkup(row_width=1)

start_support_link = InlineKeyboardButton(text="👨🏻‍💻 Поддержка", url=SUPPORT_LINK)
profile_start_button = InlineKeyboardButton(text="👤 Мой профиль", callback_data="profile")
FAQ_start_button = InlineKeyboardButton(text="❔ FAQ", callback_data=faq_callback.new(
    command_name="show_faq",
    start=0,
    end=8
))

start_keyboard.insert(profile_start_button)
start_keyboard.insert(FAQ_start_button)
start_keyboard.insert(start_support_link)
