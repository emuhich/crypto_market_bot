from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from keyboards.inline.menu_keyboard import menu_keyboard
from loader import dp
from utils.db_api.db_commands import select_client, create_client


@dp.message_handler(Command("menu"), state='*')
async def show_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.delete()
    user_id = message.from_user.id
    user = await select_client(user_id)
    if not user:
        await create_client(username=message.from_user.username, telegram_id=user_id)
    await message.answer("Выберете пункт меню:", reply_markup=menu_keyboard)


@dp.callback_query_handler(text="menu", state='*')
async def show_menu_callback(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("Выберете пункт меню:", reply_markup=menu_keyboard)
