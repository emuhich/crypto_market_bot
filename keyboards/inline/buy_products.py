from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import show_product_callback, buy_product_callback


def back_to_product(pk_products, pk_sub_categories):
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="⬅️ Назад",
                                       callback_data=show_product_callback.new(command_name="show_product",
                                                                               pk_products=pk_products,
                                                                               pk_sub_categories=pk_sub_categories
                                                                               ))
    keyboard.insert(back_button)
    return keyboard


def check_payment(pk_products, pk_sub_categories, quantity):
    keyboard = InlineKeyboardMarkup(row_width=1)
    check_btc_button = InlineKeyboardButton(text="Проверить платеж BTC",
                                            callback_data=buy_product_callback.new(command_name="check_payment",
                                                                                   pk=pk_products,
                                                                                   quantity=quantity,
                                                                                   pk_sub_categories=pk_sub_categories
                                                                                   ))
    check_eth_button = InlineKeyboardButton(text="Проверить платеж ETH",
                                            callback_data=buy_product_callback.new(command_name="check_payment",
                                                                                   pk=pk_products,
                                                                                   quantity=quantity,
                                                                                   pk_sub_categories=pk_sub_categories
                                                                                   ))
    check_usd_button = InlineKeyboardButton(text="Проверить платеж USDT",
                                            callback_data=buy_product_callback.new(command_name="check_payment",
                                                                                   pk=pk_products,
                                                                                   quantity=quantity,
                                                                                   pk_sub_categories=pk_sub_categories
                                                                                   ))
    back_button = InlineKeyboardButton(text="⬅️ Назад",
                                       callback_data=show_product_callback.new(command_name="show_product",
                                                                               pk_products=pk_products,
                                                                               pk_sub_categories=pk_sub_categories
                                                                               ))
    keyboard.insert(check_btc_button)
    keyboard.insert(check_eth_button)
    keyboard.insert(check_usd_button)
    keyboard.insert(back_button)
    return keyboard
