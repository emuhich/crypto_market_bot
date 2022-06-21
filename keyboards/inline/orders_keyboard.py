from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import my_order_callback, show_orders_callback

keyboard_my_orders = InlineKeyboardMarkup(row_width=1)
my_orders_button = InlineKeyboardButton(text="🛒 Мои заказы", callback_data=my_order_callback.new(
    command_name="my_orders",
    start=0,
    end=8
))
keyboard_my_orders.insert(my_orders_button)


def orders_keyboard(start, end, next, back, orders):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for order in orders:
        question_button = InlineKeyboardButton(text=order.product.name,
                                               callback_data=show_orders_callback.new(command_name="show_orders",
                                                                                      pk_orders=order.pk,
                                                                                      ))
        keyboard.row(question_button)

    back_button = InlineKeyboardButton(text="← Пред", callback_data=my_order_callback.new(command_name="my_orders",
                                                                                          start=start - 8,
                                                                                          end=end - 8
                                                                                          ))
    next_button = InlineKeyboardButton(text="След →", callback_data=my_order_callback.new(command_name="my_orders",
                                                                                          start=start + 8,
                                                                                          end=end + 8
                                                                                          ))
    if next and back:
        keyboard.row(back_button, next_button)
    elif next and back is False:
        keyboard.row(next_button)
    elif back and next is False:
        keyboard.row(back_button)
    back_button = InlineKeyboardButton(text="⬅️ Назад", callback_data="menu")
    keyboard.row(back_button)
    return keyboard


def back_to_my_orders():
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="⬅️ Назад", callback_data=my_order_callback.new(
        command_name="my_orders",
        start=0,
        end=8
    ))
    keyboard.insert(back_button)
    return keyboard
