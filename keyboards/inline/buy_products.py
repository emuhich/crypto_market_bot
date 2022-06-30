from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.config import SUPPORT_LINK
from keyboards.inline.callback_datas import show_product_callback, check_payment_callback, choice_payment_callback, \
    buy_product_callback


def quantity_keyboard(pk_products, pk_sub_categories, quantity, number):
    keyboard = InlineKeyboardMarkup(row_width=3)
    minus_quantity = InlineKeyboardButton(text="◀️", callback_data=buy_product_callback.new(command_name="buy_product",
                                                                                            pk_sub_categories=pk_sub_categories,
                                                                                            pk=pk_products,
                                                                                            quantity=quantity,
                                                                                            number=number - 1
                                                                                            ))
    quantity_button = InlineKeyboardButton(text=f"{number}",
                                           callback_data=buy_product_callback.new(command_name="buy_product",
                                                                                  pk_sub_categories=pk_sub_categories,
                                                                                  pk=pk_products,
                                                                                  quantity=quantity,
                                                                                  number=1
                                                                                  ))
    plus_quantity = InlineKeyboardButton(text="▶️", callback_data=buy_product_callback.new(command_name="buy_product",
                                                                                           pk_sub_categories=pk_sub_categories,
                                                                                           pk=pk_products,
                                                                                           quantity=quantity,
                                                                                           number=number + 1
                                                                                           ))
    next_button = InlineKeyboardButton(text="Продолжить",
                                       callback_data=buy_product_callback.new(command_name="confirm_pay",
                                                                              pk_sub_categories=pk_sub_categories,
                                                                              pk=pk_products,
                                                                              quantity=quantity,
                                                                              number=number + 1
                                                                              ))
    back_button = InlineKeyboardButton(text="⬅️ Назад",
                                       callback_data=show_product_callback.new(command_name="show_product",
                                                                               pk_products=pk_products,
                                                                               pk_sub_categories=pk_sub_categories
                                                                               ))
    keyboard.row(minus_quantity, quantity_button, plus_quantity)
    keyboard.row(next_button)
    keyboard.row(back_button)
    return keyboard


def back_to_product(pk_products, pk_sub_categories):
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="⬅️ Назад",
                                       callback_data=show_product_callback.new(command_name="show_product",
                                                                               pk_products=pk_products,
                                                                               pk_sub_categories=pk_sub_categories
                                                                               ))
    keyboard.insert(back_button)
    return keyboard


def choice_payment(pk_products, pk_sub_categories, quantity, number):
    keyboard = InlineKeyboardMarkup(row_width=1)
    btc_button = InlineKeyboardButton(text="Оплатить в BTC", callback_data=choice_payment_callback.new(
        command_name="choice_payment",
        coin="BTC",
        pk=pk_products,
        quantity=quantity,
        pk_sub_categories=pk_sub_categories,
        number=number
    ))
    eth_button = InlineKeyboardButton(text="Оплатить в ETH", callback_data=choice_payment_callback.new(
        command_name="choice_payment",
        coin="ETH",
        pk=pk_products,
        quantity=quantity,
        pk_sub_categories=pk_sub_categories,
        number=number
    ))
    usdt_button = InlineKeyboardButton(text="Оплатить в USDT", callback_data=choice_payment_callback.new(
        command_name="choice_payment",
        coin="USDT",
        pk=pk_products,
        quantity=quantity,
        pk_sub_categories=pk_sub_categories,
        number=number
    ))
    back_button = InlineKeyboardButton(text="⬅️ Назад",
                                       callback_data=show_product_callback.new(command_name="show_product",
                                                                               pk_products=pk_products,
                                                                               pk_sub_categories=pk_sub_categories
                                                                               ))
    keyboard.insert(btc_button)
    keyboard.insert(eth_button)
    keyboard.insert(usdt_button)
    keyboard.insert(back_button)
    return keyboard


def check_payment(pk_products, pk_sub_categories, quantity, amount, coin):
    keyboard = InlineKeyboardMarkup(row_width=1)
    check_btc_button = InlineKeyboardButton(text="Проверить платеж",
                                            callback_data=check_payment_callback.new(command_name="check_payment",
                                                                                     pk=pk_products,
                                                                                     quantity=quantity,
                                                                                     coin=coin,
                                                                                     price=amount,
                                                                                     pk_sub_categories=pk_sub_categories
                                                                                     ))
    back_button = InlineKeyboardButton(text="⬅️ Назад",
                                       callback_data=show_product_callback.new(command_name="show_product",
                                                                               pk_products=pk_products,
                                                                               pk_sub_categories=pk_sub_categories
                                                                               ))
    keyboard.insert(check_btc_button)
    keyboard.insert(back_button)
    return keyboard


def confirm_payment(pk, quantity, price, coin, pk_sub_categories):
    keyboard = InlineKeyboardMarkup(row_width=1)
    check_button = InlineKeyboardButton(text="Проверить платеж",
                                        callback_data=check_payment_callback.new(command_name="check_payment",
                                                                                 pk=pk,
                                                                                 quantity=quantity,
                                                                                 coin=coin,
                                                                                 price=price,
                                                                                 pk_sub_categories=pk_sub_categories
                                                                                 ))
    support_button = InlineKeyboardButton(text="👨🏻‍💻 Поддержка", url=SUPPORT_LINK)
    keyboard.insert(check_button)
    keyboard.insert(support_button)
    return keyboard


def payment_not_found(pk, quantity, price, coin, pk_sub_categories):
    keyboard = InlineKeyboardMarkup(row_width=1)
    check_button = InlineKeyboardButton(text="Проверить платеж",
                                        callback_data=check_payment_callback.new(command_name="check_payment",
                                                                                 pk=pk,
                                                                                 quantity=quantity,
                                                                                 coin=coin,
                                                                                 price=price,
                                                                                 pk_sub_categories=pk_sub_categories
                                                                                 ))
    support_button = InlineKeyboardButton(text="👨🏻‍💻 Поддержка", url=SUPPORT_LINK)
    back_button = InlineKeyboardButton(text="⬅️ Назад к товару",
                                       callback_data=show_product_callback.new(command_name="show_product",
                                                                               pk_products=pk,
                                                                               pk_sub_categories=pk_sub_categories
                                                                               ))
    keyboard.insert(check_button)
    keyboard.insert(support_button)
    keyboard.insert(back_button)
    return keyboard
