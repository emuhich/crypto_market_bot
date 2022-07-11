from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from handlers.users.tools import get_button_next_back
from keyboards.inline.callback_datas import catalog_callback, sub_category_callback, show_product_callback, \
    characteristic_callback
from keyboards.inline.catalog_keyboard import catalog_keyboard, back_to_menu, category_keyboard, sub_category_keyboard, \
    product_keyboard, back_to_category, back_to_sub_category, characteristic_keyboard
from loader import dp
from utils.db_api.db_commands import get_all_category, get_category, get_sub_categories, get_sub_category, get_products, \
    get_product, products_by_characteristic


@dp.callback_query_handler(catalog_callback.filter(command_name="category"))
async def show_all_category(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    categories = await get_all_category()
    if not categories:
        await call.message.edit_text(text="\n".join(
            [
                f'🗂 {hbold(f"Каталог")}\n',
                f'Кажется в каталоге нет категорий.'
                f'😌 Но скоро они появятся, заходите почаще! 🚀.',

            ]
        ), reply_markup=back_to_menu())
        return
    start = int(callback_data.get("start"))
    end = int(callback_data.get("end"))
    next, back = await get_button_next_back(len(categories), end, start)
    categories = categories[start:end]
    await call.message.edit_text(text="\n".join(
        [
            f'🗂 {hbold(f"Каталог")}\n',
            f'Выберете нужную категорию',

        ]
    ), reply_markup=catalog_keyboard(start=start, end=end, next=next, back=back, categories=categories))


@dp.callback_query_handler(sub_category_callback.filter(command_name="sub_category"))
async def show_sub_category(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    pk = int(callback_data.get("pk"))
    start = int(callback_data.get("start"))
    end = int(callback_data.get("end"))
    category = await get_category(pk)
    sub_categories = await get_sub_categories(pk)
    if not sub_categories:
        await call.message.edit_text(text="\n".join(
            [
                f'{hbold(category.title)}\n',
                f'Кажется в категории нет под категорий.'
                f'😌 Но скоро они появятся, заходите почаще! 🚀.',

            ]
        ), reply_markup=back_to_category())
        return
    next, back = await get_button_next_back(len(sub_categories), end, start)
    sub_categories = sub_categories[start:end]
    await call.message.edit_text(text="\n".join(
        [
            f'{hbold(category.title)}\n',
        ]
    ), reply_markup=category_keyboard(start=start, end=end, next=next, back=back, sub_categories=sub_categories, pk=pk))


@dp.callback_query_handler(sub_category_callback.filter(command_name="products"))
async def show_all_sub_category(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    count_keys = 0
    await state.update_data(count_keys=count_keys)
    pk = int(callback_data.get("pk"))
    sub_category = await get_sub_category(pk)
    products = await get_products(pk)
    if not products:
        await call.message.edit_text(text="\n".join(
            [
                f'{hbold(sub_category.title)}\n',
                f'Кажется мы не нашли товаров.'
                f'😌 Но скоро они появятся, заходите почаще! 🚀.',

            ]
        ), reply_markup=back_to_sub_category(pk))
        return
    name_characteristic = list(products[0].characteristics.keys())[count_keys]
    list_characteristic = [product.characteristics[name_characteristic] for product in products]
    await call.message.edit_text(text="\n".join(
        [
            f'{hbold(f"Выберите {name_characteristic}")}'
        ]
    ), reply_markup=characteristic_keyboard(set(list_characteristic), name_characteristic, pk))


@dp.callback_query_handler(characteristic_callback.filter(command="about"))
async def show_characteristic(call: CallbackQuery, callback_data: dict, state: FSMContext):
    pk = int(callback_data.get("pk"))
    keys = callback_data.get("keys")
    value = callback_data.get("value")
    start = int(callback_data.get("start"))
    end = int(callback_data.get("end"))
    await state.update_data({keys: value})
    data = await state.get_data()
    count_keys = data.get("count_keys")
    products = await get_products(pk)
    product = products[0]
    dict_characteristic = {}
    for number in range(count_keys + 1):
        list_characteristic = list(product.characteristics.keys())
        keys = list_characteristic[number]
        value = data.get(keys)
        dict_characteristic.update({keys: value})
    products = await products_by_characteristic(pk, dict_characteristic)
    len_characteristic = len(products[0].characteristics)
    if count_keys >= len_characteristic - 1:
        sub_category = await get_sub_category(pk)
        next, back = await get_button_next_back(len(products), end, start)
        products = products[start:end]
        await call.message.edit_text(text="\n".join(
            [
                f'{hbold(sub_category.title)}\n',
            ]
        ), reply_markup=sub_category_keyboard(start=start, end=end, next=next, back=back, products=products, pk=pk,
                                              keys=keys, value=value))
        return
    name_characteristic = list(products[0].characteristics.keys())[count_keys + 1]
    list_characteristic = [product.characteristics[name_characteristic] for product in products]
    await state.update_data(count_keys=count_keys + 1)
    await call.message.edit_text(text="\n".join(
        [
            f'{hbold(f"Выберите {name_characteristic}")}'
        ]
    ), reply_markup=characteristic_keyboard(set(list_characteristic), name_characteristic, pk))


@dp.callback_query_handler(characteristic_callback.filter(command="back_char"))
async def back_characteristic(call: CallbackQuery, callback_data: dict, state: FSMContext):
    pk = int(callback_data.get("pk"))
    keys = callback_data.get("keys")
    value = callback_data.get("value")
    start = int(callback_data.get("start"))
    end = int(callback_data.get("end"))
    await state.update_data({keys: value})
    data = await state.get_data()
    count_keys = data.get("count_keys") - 1
    if count_keys < 0:
        return await show_sub_category(call, callback_data, state)
    products = await get_products(pk)
    product = products[0]
    dict_characteristic = {}
    for number in range(count_keys):
        list_characteristic = list(product.characteristics.keys())
        keys = list_characteristic[number]
        value = data.get(keys)
        dict_characteristic.update({keys: value})
    products = await products_by_characteristic(pk, dict_characteristic)
    len_characteristic = len(products[0].characteristics)
    if count_keys >= len_characteristic - 1:
        sub_category = await get_sub_category(pk)
        next, back = await get_button_next_back(len(products), end, start)
        products = products[start:end]
        await call.message.edit_text(text="\n".join(
            [
                f'{hbold(sub_category.title)}\n',
            ]
        ), reply_markup=sub_category_keyboard(start=start, end=end, next=next, back=back, products=products, pk=pk,
                                              keys=keys, value=value))
        return
    name_characteristic = list(products[0].characteristics.keys())[count_keys]
    list_characteristic = [product.characteristics[name_characteristic] for product in products]
    await state.update_data(count_keys=count_keys)
    await call.message.edit_text(text="\n".join(
        [
            f'{hbold(f"Выберите {name_characteristic}")}'
        ]
    ), reply_markup=characteristic_keyboard(set(list_characteristic), name_characteristic, pk))


@dp.callback_query_handler(sub_category_callback.filter(command_name="back_products"))
async def show_all_sub_category(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    pk = int(callback_data.get("pk"))
    data = await state.get_data()
    count_keys = data.get("count_keys") + 1
    start = 0
    end = 8
    products = await get_products(pk)
    product = products[0]
    dict_characteristic = {}
    for number in range(count_keys):
        list_characteristic = list(product.characteristics.keys())
        keys = list_characteristic[number]
        value = data.get(keys)
        dict_characteristic.update({keys: value})
    products = await products_by_characteristic(pk, dict_characteristic)
    sub_category = await get_sub_category(pk)
    next, back = await get_button_next_back(len(products), end, start)
    products = products[start:end]
    await call.message.answer(text="\n".join(
        [
            f'{hbold(sub_category.title)}\n',
        ]
    ), reply_markup=sub_category_keyboard(start=start, end=end, next=next, back=back, products=products, pk=pk,
                                          keys=keys, value=value))
    return


@dp.callback_query_handler(show_product_callback.filter(command_name="show_product"), state="*")
async def show_products(call: CallbackQuery, callback_data: dict):
    await call.message.delete()
    pk_products = int(callback_data.get("pk_products"))
    pk_sub_categories = int(callback_data.get("pk_sub_categories"))
    product = await get_product(pk_products)
    number = int(callback_data.get("number"))
    if number > product.quantity:
        number = 1
    if number < 1:
        number = product.quantity
    await call.message.answer_photo(photo=product.image, caption="\n".join(
        [
            f'{hbold(product.name)}\n',
            f'{hbold("Описание:")}\n {product.description}\n',
            f'{hbold("Цена:")} {product.price} USDT.\n',
            f'{hbold("В наличии:")} {product.quantity} шт.',

        ]
    ), reply_markup=product_keyboard(pk_sub_categories, pk_products, product.quantity, number))
