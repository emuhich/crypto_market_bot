from decimal import Decimal

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold, hlink, hcode

from data.config import SUPPORT_LINK
from keyboards.inline.buy_products import back_to_product, check_payment, confirm_payment, payment_not_found, \
    choice_payment
from keyboards.inline.callback_datas import buy_product_callback, check_payment_callback, choice_payment_callback
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
    product = await get_product(pk)
    try:
        client = Binance()
        commission = await client.get_rand_commission()
        commission_usd = await client.get_rand_commission_usdt()
        amount_usd = (count * product.price) + commission_usd
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
                f'Сумма в BTC: {amount_btc}',
                f'Сумма в ETH: {amount_eth}',
                f'Сумма в USDT: {amount_usd}\n',
                hbold('Выберете способ оплаты которым хотите оплатить')

            ]
        ), reply_markup=choice_payment(pk_products=pk, pk_sub_categories=pk_sub_categories)
    )
    await state.update_data(count=count)


@dp.callback_query_handler(choice_payment_callback.filter(command_name="choice_payment"))
async def buy_product(call: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    pk = data.get("pk")
    pk_sub_categories = data.get("pk_sub_categories")
    quantity = data.get("quantity")
    count = data.get("count")
    coin = int(callback_data.get("coin"))
    if count > quantity:
        await call.message.edit_text(text="\n".join(
            [
                f'{hbold(f"❌ Ошибка.")}\n',
                f'К сожалению товар закаончился',

            ]
        ), reply_markup=back_to_product(pk, pk_sub_categories))
        return
    await state.finish()
    product = await get_product(pk)
    try:
        client = Binance()
        commission = await client.get_rand_commission()
        commission_usd = await client.get_rand_commission_usdt()
        amount_usd = (count * product.price) + commission_usd
        amount_btc, amount_eth = await client.get_price_btc_eth(count * product.price)
        amount_btc += commission
        amount_eth += commission
    except Exception:
        await call.message.edit_text(f"❌ Произошла ошибка при подключении к бинанс,"
                                     f"Попробуйте позже или напишите в {hlink('техх пооддержку', SUPPORT_LINK)}",
                                     reply_markup=back_to_product(pk, pk_sub_categories))
        return
    string = [f'{hbold(f"Платежные данные {coin}")}']
    if coin == "BTC":
        amount = amount_btc
        string.append(f'Сумма: {amount}\n')
        string.append(f'Адресс кошелька: \n{hcode("1MhT6depTHHwGjXKVhKDKfszP6a3rHMoeN")}')
    elif coin == "ETH":
        amount = amount_eth
        string.append(f'Сумма: {amount}')
        string.append(f'Кошельки: \n')
        string.append(f'BEP20')
        string.append(hcode("0x1eb153b1723166ebce846d10d61123396998d75c\n"))
        string.append(f'ERC20')
        string.append(hcode("0x1eb153b1723166ebce846d10d61123396998d75c\n"))
    else:
        amount = amount_usd
        string.append(f'Сумма: {amount}')
        string.append(f'Кошельки: \n')
        string.append(f'BEP20')
        string.append(hcode("0x1eb153b1723166ebce846d10d61123396998d75c\n"))
        string.append(f'BEP 2')
        string.append(hcode("bnb136ns6lfw4zs5hg4n85vdthaad7hq5m4gtkgf23E\n"))
        string.append(f'ERC20')
        string.append(hcode("0x1eb153b1723166ebce846d10d61123396998d75c\n"))
        string.append(f'TRC20')
        string.append(hcode("TJe8ToeneKfQsFGfYnBy3nF2zfQwaZ5y4qR\n"))
    string.append(hbold('⚠️ Важно при каждом платеже генерируется уникальная комиссия, она никак не '
                        'влияет на итоговую сумму, но помогает нам отследить платеж, поэтому сумма должна совпадать'
                        'до каждой цифры.\n'), )
    string.append(f'После оплаты нажмите кнопку «Проверить платеж», деньги могут прийти не моментально.')
    await call.message.edit_text(text="\n".join(string),
                                 reply_markup=check_payment(pk_products=pk, pk_sub_categories=pk_sub_categories,
                                                            quantity=quantity, amount=amount, coin=coin))


@dp.callback_query_handler(check_payment_callback.filter(command_name="check_payment"))
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
