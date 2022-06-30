from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from keyboards.inline.start_keyboard import start_keyboard
from loader import dp
from utils.db_api.db_commands import create_client, check_client


@dp.message_handler(CommandStart(), state='*')
async def bot_start_no_state(message: types.Message, state: FSMContext):
    await message.delete()
    await state.finish()
    user_id = message.from_user.id
    user = await check_client(user_id)
    if not user:
        await create_client(username=message.from_user.username, telegram_id=user_id)

    await message.answer(text="\n".join(
        [
            f'Добро пожаловать в Cryptomarketplace, здесь '
            f'Вы можете приобрести наиболее востребованные '
            f'товары на рынке по конкурентным ценам, используя криптовалюту.'
            f'Пожалуйста, заполните свой профиль для дальнейшего удобства оформления заказов',

        ]
    ), reply_markup=start_keyboard)
