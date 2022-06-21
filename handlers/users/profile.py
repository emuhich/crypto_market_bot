from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from keyboards.inline.profile import profile_keyboard, back_to_profile
from loader import dp
from states.states import States
from utils.db_api.db_commands import select_client, update_client_info


@dp.callback_query_handler(text="profile", state='*')
async def show_menu_callback(call: CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = call.message.chat.id
    user = await select_client(user_id)
    if not user.phone:
        phone = f"{hbold('⚠️ Не установлен')}"
    else:
        phone = user.phone
    if not user.address:
        address = f"{hbold('⚠️ Не установлен')}"
    else:
        address = user.address
    if not user.full_name:
        full_name = f"{hbold('⚠️ Не установлено')}"
    else:
        full_name = user.full_name

    await call.message.edit_text(text="\n".join(
        [
            f'👤 {hbold(f"Мой профиль")}\n',
            f'{hbold("ФИО:")} {full_name}\n',
            f'{hbold("Адрес:")} {address}\n',
            f'{hbold("Телефон:")} {phone}\n',
            f'Для совершения покупок установите Адрес, ФИО и номер телефона по которому с вами можно связаться',

        ]
    ), reply_markup=profile_keyboard())


@dp.callback_query_handler(text="change_fio")
async def show_menu_callback(call: CallbackQuery):
    user_id = call.message.chat.id
    user = await select_client(user_id)
    if not user.full_name:
        full_name = f"{hbold('⚠️ Не установлено')}"
    else:
        full_name = user.full_name

    await call.message.edit_text(text="\n".join(
        [
            f'{hbold(f"🏷 Изменить ФИО")}\n',
            f'{hbold("Текущее ФИО:")} {full_name}\n',
            f'Введите новое ФИО под этим сообщением.\n',
            f'✅ Пример: Соколов Антон Антонович',

        ]
    ), reply_markup=back_to_profile())
    await States.CHANGE_FIO.set()


@dp.message_handler(state=States.CHANGE_FIO)
async def set_fbs_api(message: types.Message):
    await message.delete()
    user_id = message.from_user.id
    fio = message.text
    user = await update_client_info(telegram_id=user_id, fio=fio)
    if not user.full_name:
        full_name = f"{hbold('⚠️ Не установлено')}"
    else:
        full_name = user.full_name

    await message.answer(text="\n".join(
        [
            f'{hbold(f"🏷 Изменить ФИО")}\n',
            f'{hbold("Текущее ФИО:")} {full_name}\n',
            f'Введите новое ФИО под этим сообщением.\n',
            f'✅ Пример: Соколов Антон Антонович',

        ]
    ), reply_markup=back_to_profile())


@dp.callback_query_handler(text="change_address")
async def show_menu_callback(call: CallbackQuery):
    user_id = call.message.chat.id
    user = await select_client(user_id)
    if not user.address:
        address = f"{hbold('⚠️ Не установлен')}"
    else:
        address = user.address

    await call.message.edit_text(text="\n".join(
        [
            f'{hbold(f"📨 Изменить Адрес")}\n',
            f'{hbold("Текущий Адрес:")} {address}\n',
            f'Введите новый адрес под этим сообшением.\n',
            f'✅ Пример: Большая Никитская улица, г.Москва д.8, кв.56',

        ]
    ), reply_markup=back_to_profile())
    await States.CHANGE_ADDRESS.set()


@dp.message_handler(state=States.CHANGE_ADDRESS)
async def set_fbs_api(message: types.Message):
    await message.delete()
    user_id = message.from_user.id
    address = message.text
    user = await update_client_info(telegram_id=user_id, address=address)
    if not user.address:
        address = f"{hbold('⚠️ Не установлено')}"
    else:
        address = user.address

    await message.answer(text="\n".join(
        [
            f'{hbold(f"📨 Изменить Адрес")}\n',
            f'{hbold("Текущий Адрес:")} {address}\n',
            f'Введите новый адрес под этим сообщением.\n',
            f'✅ Пример: Большая Никитская улица, г.Москва д.8, кв.56',

        ]
    ), reply_markup=back_to_profile())


@dp.callback_query_handler(text="change_phone")
async def show_menu_callback(call: CallbackQuery):
    user_id = call.message.chat.id
    user = await select_client(user_id)
    if not user.phone:
        phone = f"{hbold('⚠️ Не установлен')}"
    else:
        phone = user.phone

    await call.message.edit_text(text="\n".join(
        [
            f'{hbold(f"📱 Изменить телефон")}\n',
            f'{hbold("Текущий телефон:")} {phone}\n',
            f'Введите новый телефон под этим сообщением.\n',
            f'✅ Пример: 79779567811',

        ]
    ), reply_markup=back_to_profile())
    await States.CHANGE_PHONE.set()


@dp.message_handler(state=States.CHANGE_PHONE)
async def set_fbs_api(message: types.Message):
    await message.delete()
    user_id = message.from_user.id
    phone = message.text
    user = await update_client_info(telegram_id=user_id, phone=phone)
    if not user.phone:
        phone = f"{hbold('⚠️ Не установлено')}"
    else:
        phone = user.phone

    await message.answer(text="\n".join(
        [
            f'{hbold(f"📱 Изменить телефон")}\n',
            f'{hbold("Текущий телефон:")} {phone}\n',
            f'Введите новый телефон под этим сообщением.\n',
            f'✅ Пример: 79779567811',

        ]
    ), reply_markup=back_to_profile())
