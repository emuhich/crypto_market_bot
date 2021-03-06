from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import catalog_callback, sub_category_callback, show_product_callback, \
    buy_product_callback, characteristic_callback


def catalog_keyboard(start, end, next, back, categories):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for category in categories:
        question_button = InlineKeyboardButton(text=category.title,
                                               callback_data=sub_category_callback.new(command_name="sub_category",
                                                                                       pk=category.pk,
                                                                                       start=0,
                                                                                       end=8
                                                                                       ))
        keyboard.row(question_button)

    back_button = InlineKeyboardButton(text="← Пред", callback_data=catalog_callback.new(command_name="category",
                                                                                         start=start - 8,
                                                                                         end=end - 8
                                                                                         ))
    next_button = InlineKeyboardButton(text="След →", callback_data=catalog_callback.new(command_name="category",
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


def category_keyboard(start, end, next, back, sub_categories, pk):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for sub_category in sub_categories:
        question_button = InlineKeyboardButton(text=sub_category.title,
                                               callback_data=sub_category_callback.new(command_name="products",
                                                                                       pk=sub_category.pk,
                                                                                       start=0,
                                                                                       end=8
                                                                                       ))
        keyboard.row(question_button)

    back_button = InlineKeyboardButton(text="← Пред",
                                       callback_data=sub_category_callback.new(command_name="sub_category",
                                                                               pk=pk,
                                                                               start=start - 8,
                                                                               end=end - 8
                                                                               ))
    next_button = InlineKeyboardButton(text="След →",
                                       callback_data=sub_category_callback.new(command_name="sub_category",
                                                                               pk=pk,
                                                                               start=start + 8,
                                                                               end=end + 8
                                                                               ))
    if next and back:
        keyboard.row(back_button, next_button)
    elif next and back is False:
        keyboard.row(next_button)
    elif back and next is False:
        keyboard.row(back_button)
    back_button = InlineKeyboardButton(text="⬅️ Назад", callback_data=catalog_callback.new(
        command_name="category",
        start=0,
        end=8
    ))
    keyboard.row(back_button)
    return keyboard


def sub_category_keyboard(start, end, next, back, products, pk, keys, value):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for product in products:
        question_button = InlineKeyboardButton(text=product.name,
                                               callback_data=show_product_callback.new(command_name="show_product",
                                                                                       pk_products=product.pk,
                                                                                       pk_sub_categories=pk,
                                                                                       number=1
                                                                                       ))
        keyboard.row(question_button)

    back_button = InlineKeyboardButton(text="← Пред",
                                       callback_data=sub_category_callback.new(command_name="products",
                                                                               pk=pk,
                                                                               start=start - 8,
                                                                               end=end - 8
                                                                               ))
    next_button = InlineKeyboardButton(text="След →",
                                       callback_data=sub_category_callback.new(command_name="products",
                                                                               pk=pk,
                                                                               start=start + 8,
                                                                               end=end + 8
                                                                               ))
    if next and back:
        keyboard.row(back_button, next_button)
    elif next and back is False:
        keyboard.row(next_button)
    elif back and next is False:
        keyboard.row(back_button)
    back_button = InlineKeyboardButton(text="⬅️ Назад", callback_data=characteristic_callback.new(
        command="back_char",
        start=0,
        end=8,
        keys=keys,
        value=value,
        pk=pk
    ))
    keyboard.row(back_button)
    return keyboard


def product_keyboard(pk_sub_categories, pk_product, quantity, number):
    keyboard = InlineKeyboardMarkup(row_width=1)
    bay_button = InlineKeyboardButton(text="💳 Купить",
                                      callback_data=buy_product_callback.new(command_name="confirm_pay",
                                                                             pk_sub_categories=pk_sub_categories,
                                                                             pk=pk_product,
                                                                             quantity=quantity,
                                                                             number=number,
                                                                             ))
    minus_quantity = InlineKeyboardButton(text="◀️",
                                          callback_data=show_product_callback.new(command_name="show_product",
                                                                                  pk_products=pk_product,
                                                                                  pk_sub_categories=pk_sub_categories,
                                                                                  number=number - 1
                                                                                  ))
    quantity_button = InlineKeyboardButton(text=f"{number} шт.",
                                           callback_data=show_product_callback.new(command_name="show_product",
                                                                                   pk_products=pk_product,
                                                                                   pk_sub_categories=pk_sub_categories,
                                                                                   number=1
                                                                                   ))
    plus_quantity = InlineKeyboardButton(text="▶️", callback_data=show_product_callback.new(command_name="show_product",
                                                                                            pk_products=pk_product,
                                                                                            pk_sub_categories=pk_sub_categories,
                                                                                            number=number + 1
                                                                                            ))
    back_button = InlineKeyboardButton(text="⬅️ Назад",
                                       callback_data=sub_category_callback.new(command_name="back_products",
                                                                               pk=pk_sub_categories,
                                                                               start=0,
                                                                               end=8
                                                                               ))

    keyboard.row(bay_button)
    keyboard.row(minus_quantity, quantity_button, plus_quantity)
    keyboard.row(back_button)
    return keyboard


def back_to_category():
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="⬅️ Назад", callback_data=catalog_callback.new(
        command_name="category",
        start=0,
        end=8
    ))
    keyboard.insert(back_button)
    return keyboard


def back_to_sub_category(pk):
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="⬅️ Назад", callback_data=sub_category_callback.new(
        command_name="sub_category",
        pk=pk,
        start=0,
        end=8
    ))
    keyboard.insert(back_button)
    return keyboard


def back_to_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text="⬅️ Назад", callback_data="menu")
    keyboard.row(back_button)
    return keyboard


def characteristic_keyboard(list_characteristic, name_characteristic, pk):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for i in list_characteristic:
        button = InlineKeyboardButton(text=i, callback_data=characteristic_callback.new(
            command="about",
            start=0,
            end=8,
            keys=name_characteristic,
            value=i,
            pk=pk
        ))
        keyboard.insert(button)

    back_button = InlineKeyboardButton(text="⬅️ Назад", callback_data=characteristic_callback.new(
        command="back_char",
        start=0,
        end=8,
        keys=name_characteristic,
        value=i,
        pk=pk
    ))
    keyboard.insert(back_button)

    return keyboard
