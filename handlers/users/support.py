from unittest.mock import call

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandHelp
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from keyboards.inline.support_keyboard import support_keyboard
from loader import dp
from utils.misc import rate_limit


@dp.callback_query_handler(text="support", state='*')
async def show_menu_callback(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(text="\n".join(
        [
            f'{hbold(f"👨🏻‍💻 Поддержка")}\n',
            f'В случае возникновения вопросов, контакты:\n',
            f'Телефон: +79999681343 (Савва)'
            f'Почта: cryptomarketplace.msk@gmail.com',
        ]
    ), reply_markup=support_keyboard)


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="\n".join(
        [
            f'{hbold(f"👨🏻‍💻 Поддержка")}\n',
            f'В случае возникновения вопросов, контакты:\n',
            f'Телефон: +79999681343 (Савва)'
            f'Почта: cryptomarketplace.msk@gmail.com',
        ]
    ), reply_markup=support_keyboard)
