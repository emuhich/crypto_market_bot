from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def profile_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    change_fio = InlineKeyboardButton(text="🏷 Изменить ФИО", callback_data="change_fio")
    change_address = InlineKeyboardButton(text="📨 Изменить Адрес", callback_data="change_address")
    change_phone = InlineKeyboardButton(text="📱 Изменить телефон", callback_data="change_phone")
    back_button = InlineKeyboardButton(text="⬅️ Назад", callback_data="menu")

    keyboard.insert(change_fio)
    keyboard.insert(change_address)
    keyboard.insert(change_phone)
    keyboard.insert(back_button)
    return keyboard


def back_to_profile():
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="⬅️ Назад", callback_data="profile")
    keyboard.insert(back_button)
    return keyboard
