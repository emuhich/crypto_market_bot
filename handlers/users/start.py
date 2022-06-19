from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from keyboards.inline.start_keyboard import start_keyboard
from loader import dp
from utils.db_api.db_commands import select_client, create_client


@dp.message_handler(CommandStart(), state='*')
async def bot_start_no_state(message: types.Message, state: FSMContext):
    await message.delete()
    await state.finish()
    user_id = message.from_user.id
    user = await select_client(user_id)
    if not user:
        await create_client(username=message.from_user.username, telegram_id=user_id)

    await message.answer(text="\n".join(
        [
            f'Приветственное сообщение'
            'Тут рассказываем о сервисе,'
            'преимуществах, почему необходимо'
            'поделиться с нами своими личными'
            'данными и тд и тд',

        ]
    ), reply_markup=start_keyboard)
