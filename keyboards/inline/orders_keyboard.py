from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard_my_orders = InlineKeyboardMarkup(row_width=1)
my_orders_button = InlineKeyboardButton(text="🛒 Мои заказы", callback_data="my_orders")
keyboard_my_orders.insert(my_orders_button)
