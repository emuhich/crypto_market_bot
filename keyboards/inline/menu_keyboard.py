from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import faq_callback, catalog_callback

menu_keyboard = InlineKeyboardMarkup(row_width=1)
catalog_button = InlineKeyboardButton(text="🗂 Каталог", callback_data=catalog_callback.new(
    command_name="category",
    start=0,
    end=8
))
my_orders_button = InlineKeyboardButton(text="🛒 Мои заказы", callback_data="my_orders")
support_button = InlineKeyboardButton(text="👨🏻‍💻 Поддержка", callback_data="support")
profile_button = InlineKeyboardButton(text="👤 Мой профиль", callback_data="profile")
FAQ_button = InlineKeyboardButton(text="❔ FAQ", callback_data=faq_callback.new(
    command_name="show_faq",
    start=0,
    end=8
))

menu_keyboard.insert(catalog_button)
menu_keyboard.insert(my_orders_button)
menu_keyboard.insert(profile_button)
menu_keyboard.insert(support_button)
menu_keyboard.insert(FAQ_button)
