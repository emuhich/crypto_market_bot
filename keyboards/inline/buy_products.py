from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.config import SUPPORT_LINK
from keyboards.inline.callback_datas import show_product_callback, check_payment_callback


def back_to_product(pk_products, pk_sub_categories):
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="⬅️ Назад",
                                       callback_data=show_product_callback.new(command_name="show_product",
                                                                               pk_products=pk_products,
                                                                               pk_sub_categories=pk_sub_categories
                                                                               ))
    keyboard.insert(back_button)
    return keyboard


def check_payment(pk_products, pk_sub_categories, quantity, amount_usd, amount_btc, amount_eth):
    keyboard = InlineKeyboardMarkup(row_width=1)
    check_btc_button = InlineKeyboardButton(text="Проверить платеж BTC",
                                            callback_data=check_payment_callback.new(command_name="check_payment",
                                                                                     pk=pk_products,
                                                                                     quantity=quantity,
                                                                                     coin="BTC",
                                                                                     price=amount_btc,
                                                                                     pk_sub_categories=pk_sub_categories
                                                                                     ))
    check_eth_button = InlineKeyboardButton(text="Проверить платеж ETH",
                                            callback_data=check_payment_callback.new(command_name="check_payment",
                                                                                     pk=pk_products,
                                                                                     quantity=quantity,
                                                                                     coin="ETH",
                                                                                     price=amount_eth,
                                                                                     pk_sub_categories=pk_sub_categories
                                                                                     ))
    check_usd_button = InlineKeyboardButton(text="Проверить платеж USDT",
                                            callback_data=check_payment_callback.new(command_name="check_payment",
                                                                                     pk=pk_products,
                                                                                     quantity=quantity,
                                                                                     coin="USDT",
                                                                                     price=amount_usd,
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


def confirm_payment(pk, quantity, price, coin,pk_sub_categories):
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
