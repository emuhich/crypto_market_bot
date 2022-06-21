from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold, hlink

from data.config import SUPPORT_LINK
from keyboards.inline.buy_products import back_to_product, check_payment
from keyboards.inline.callback_datas import buy_product_callback
from keyboards.inline.orders_keyboard import keyboard_my_orders
from keyboards.inline.profile import my_profile_keyboard
from loader import dp
from states import States
from utils.db_api.db_commands import get_product, select_client, create_order
from utils.misc.binance import Binance


@dp.callback_query_handler(buy_product_callback.filter(command_name="buy_product"))
async def buy_product(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    await state.finish()
    pk = int(callback_data.get("pk"))
    quantity = int(callback_data.get("quantity"))
    pk_sub_categories = int(callback_data.get("pk_sub_categories"))
    user_id = call.message.chat.id
    user = await select_client(user_id)
    if not user.full_name or not user.address or not user.phone:
        await call.message.answer(
            text="\n".join(
                [
                    f'❌ {hbold(f"Ошибка")}\n',
                    f'Для совершения оплаты нужно заполнить личные данные:.',
                    f'- ФИО',
                    f'- Адрес доставки',
                    f'- Номер телефона по которому можно связаться\n',
                    f'Все эти данные можно указать во вкладке 👤 Мой профиль.',

                ]
            ), reply_markup=my_profile_keyboard())
        return
    await call.message.answer(text="\n".join(
        [
            f'{hbold(f"Введите количество товара")}\n',
            f'⚠️ Внимание количество товара должно быть числом выше нуля и не больше'
            f'товара в наличии - {quantity}',

        ]
    ), reply_markup=back_to_product(pk, pk_sub_categories))
    await States.QUANTITY_PRODUCTS.set()
    await state.update_data(quantity=quantity)
    await state.update_data(pk=pk)
    await state.update_data(pk_sub_categories=pk_sub_categories)


@dp.message_handler(state=States.QUANTITY_PRODUCTS)
async def get_binance_address(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    pk = data.get("pk")
    pk_sub_categories = data.get("pk_sub_categories")
    quantity = data.get("quantity")
    if not message.text.isdigit():
        await message.answer(text="\n".join(
            [
                f'{hbold(f"❌ Ошибка.")}\n',
                f'⚠️ Внимание количество товара должно быть числом выше нуля и не больше'
                f'товара в наличии - {quantity}\n',
                f'Введите новое количество товара под этим сообщением',

            ]
        ), reply_markup=back_to_product(pk, pk_sub_categories))
        return
    elif int(message.text) <= 0 or int(message.text) > quantity:
        await message.answer(text="\n".join(
            [
                f'{hbold(f"❌ Ошибка.")}\n',
                f'⚠️ Внимание количество товара должно быть числом выше нуля и не больше'
                f'товара в наличии - {quantity}\n',
                f'Введите новое количество товара под этим сообщением',

            ]
        ), reply_markup=back_to_product(pk, pk_sub_categories))
        return
    count = int(message.text)
    await state.finish()
    product = await get_product(pk)
    try:
        client = Binance()
        btc_address = await client.get_address_btc()
        eth_address = await client.get_address_eth()
        usd_address = await client.get_address_usd()
    except Exception:
        await message.answer(f"❌ Произошла ошибка при подключении к бинанс,"
                             f"Попробуйте позже или напишите в {hlink('техх пооддержку', SUPPORT_LINK)}",
                             reply_markup=back_to_product(pk, pk_sub_categories))
        return
    await message.answer(
        text="\n".join(
            [
                f'{hbold(f"✅ Оплата.")}\n',
                hbold("Заказ: "),
                f'Название: {product.name}',
                f'Количество: {count} шт',
                f'Итоговая цена: {count * product.price} USDT\n',
                f'Введите новое количество товара под этим сообщением:\n',
                f'Сумма в BTC: {count * product.price}',
                f'BTC кошелек: {btc_address}\n',
                f'Сумма в ETH: {count * product.price}',
                f'ETH кошелек: {eth_address}\n',
                f'Сумма в USDT: {count * product.price}',
                f'USDT кошелек: {usd_address}\n',
                f'После оплаты нажмите кнопку «Проверить платеж» с валютой в которой вы оплатитли.'

            ]
        ), reply_markup=check_payment(pk, pk_sub_categories, count)
    )


@dp.callback_query_handler(buy_product_callback.filter(command_name="check_payment"))
async def buy_product(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    pk = int(callback_data.get("pk"))
    quantity = int(callback_data.get("quantity"))
    pk_sub_categories = int(callback_data.get("pk_sub_categories"))
    telegram_id = call.message.chat.id
    await create_order(pk, telegram_id, quantity)
    await call.message.edit_text("\n".join(
        [
            f'{hbold(f"✅ Ваш заказ успешно создан")}\n',
            f'Отслеживать статус заказа вы можете во вкладке 🛒 Мои заказы',
            f'Так же после изменения статуса заказа вам придет уведомление.',

        ]
    ), reply_markup=keyboard_my_orders)
