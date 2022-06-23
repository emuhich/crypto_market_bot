from decimal import Decimal

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold, hlink

from data.config import SUPPORT_LINK
from keyboards.inline.buy_products import back_to_product, check_payment, confirm_payment, payment_not_found
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
        commission = await client.get_rand_commission()
        amount_usd = count * product.price + commission
        amount_btc, amount_eth = await client.get_price_btc_eth(count * product.price)
        amount_btc += commission
        amount_eth += commission
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
                f'Введите новое количество товара под этим сообщением:\n',
                f'Сумма в BTC: {amount_btc}',
                f'BTC кошелек: {btc_address}\n',
                f'Сумма в ETH: {amount_eth}',
                f'ETH кошелек: {eth_address}\n',
                f'Сумма в USDT: {amount_usd}',
                f'USDT кошелек: {usd_address}\n',
                hbold('⚠️ Важно при каждом платеже генерируется уникальная комиссия, она никак не '
                      'влияет на итоговую сумму, но помогает нам отследить платеж, поэтому сумма должна совпадать'
                      'до каждой цифры.\n'),
                f'После оплаты нажмите кнопку «Проверить платеж» с валютой в которой вы оплатитли.'

            ]
        ), reply_markup=check_payment(pk, pk_sub_categories, count, amount_usd, amount_btc, amount_eth)
    )


@dp.callback_query_handler(buy_product_callback.filter(command_name="check_payment"))
async def buy_product(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    pk = int(callback_data.get("pk"))
    quantity = int(callback_data.get("quantity"))
    coin = callback_data.get("coin")
    price = Decimal(callback_data.get("price"))
    pk_sub_categories = int(callback_data.get("pk_sub_categories"))
    client = Binance()
    result = await client.check_payment(amount=price, coin=coin)
    if result == "NotFound":
        await call.message.edit_text("\n".join(
            [
                f'{hbold(f"❌ Платеж не найден")}\n',
                f'Мы не нашли ваш платеж, если вы оплатитли нажмите кнопку проверить платеж снизу,'
                f'через 10 минут, или обратитесь в техх поддержку.',
                hbold('⚠️ Проверить платежно можно будет только по кнопке снизу ❗️')
            ]
        ), reply_markup=payment_not_found(pk, quantity, price, coin, pk_sub_categories)
        )
        return
    if result == "NotConfirmed":
        await call.message.edit_text("\n".join(
            [
                f'{hbold(f"⚠️ Платеж найден, но еще не подтвержден")}\n',
                f'Проверьте оплату позже',
                hbold('⚠️ Проверить платежно можно будет только по кнопке снизу ❗️')
            ]
        ), reply_markup=confirm_payment(pk, quantity, price, coin, pk_sub_categories)
        )
        return
    telegram_id = call.message.chat.id
    await create_order(pk, telegram_id, quantity)
    await call.message.edit_text("\n".join(
        [
            f'{hbold(f"✅ Ваш заказ успешно создан")}\n',
            f'Отслеживать статус заказа вы можете во вкладке 🛒 Мои заказы',
            f'Так же после изменения статуса заказа вам придет уведомление.',

        ]
    ), reply_markup=keyboard_my_orders)
