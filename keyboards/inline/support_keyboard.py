from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import SUPPORT_LINK

support_keyboard = InlineKeyboardMarkup(row_width=1)

support_button = InlineKeyboardButton(text="👨🏻‍💻 Чат с подержкой", url=SUPPORT_LINK)
back_to_menu = InlineKeyboardButton(text="⬅️ Назад", callback_data="menu")
support_keyboard.insert(support_button)
support_keyboard.insert(back_to_menu)
