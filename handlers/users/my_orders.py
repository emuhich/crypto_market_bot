from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from handlers.users.tools import get_button_next_back
from keyboards.inline.callback_datas import my_order_callback, show_orders_callback
from keyboards.inline.catalog_keyboard import back_to_menu
from keyboards.inline.orders_keyboard import orders_keyboard, back_to_my_orders
from loader import dp
from utils.db_api.db_commands import get_orders_by_user_id, get_order


@dp.callback_query_handler(my_order_callback.filter(command_name="my_orders"))
async def show_my_orders(call: CallbackQuery, callback_data: dict):
    start = int(callback_data.get("start"))
    end = int(callback_data.get("end"))
    user_id = call.message.chat.id
    orders = await get_orders_by_user_id(user_id)
    if not orders:
        await call.message.edit_text(text="\n".join(
            [
                f'🛒 {hbold(f"Мои заказы")}\n',
                f'Кажется мы не нашли у вас заказов.',
                f'Как только совершите заказ он обязательно появится здесь.',

            ]
        ), reply_markup=back_to_menu())
        return
    next, back = await get_button_next_back(len(orders), end, start)
    orders = orders[start:end]
    await call.message.edit_text(text="\n".join(
        [
            f'🛒 {hbold(f"Мои заказы")}\n',
            f'Снизу история ваших заказов',
            f'Нажмите на заказ чтобы получить подробную информацию',

        ]
    ), reply_markup=orders_keyboard(start=start, end=end, next=next, back=back, orders=orders))


@dp.callback_query_handler(show_orders_callback.filter(command_name="show_orders"))
async def show_order(call: CallbackQuery, callback_data: dict):
    pk_orders = int(callback_data.get("pk_orders"))
    order = await get_order(pk_orders)
    if order.status == 'accepted':
        status = "принят в обработку"
    elif order.status == 'processed':
        status = "обработан"
    elif order.status == 'in_delivery':
        status = "передан в доставку"
    else:
        status = "доставлен"
    date_order = order.created.strftime("%Y-%m-%d %H:%M:%S")
    change_date = order.updated.strftime("%Y-%m-%d %H:%M:%S")
    string = [
        f'🛒 {hbold(f"Мои заказы")}\n',
        f'{hbold("Название товара:")} {order.product.name}',
        f'{hbold("Цена за штуку:")} {order.product.price} USDT',
        f'{hbold("Аддресс доставки:")} {order.address}',
        f'{hbold("Количество:")} {order.quantity}',
        f'{hbold("Итоговая цена:")} {order.price} USDT\n',
        f'{hbold("Текущий статус:")} {status}\n',
        f'{hbold("Дата совершения заказа:")} {date_order}',

    ]
    if status == "доставлен":
        string.append(f'{hbold("Дата доставки:")} {change_date}', )
    else:
        string.append(f'{hbold("Последнее изменение статуса:")} {change_date}', )
    await call.message.edit_text(text="\n".join(string), reply_markup=back_to_my_orders())
