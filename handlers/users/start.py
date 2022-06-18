from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from loader import dp
from utils.db_api.db_commands import select_client, create_client


@dp.message_handler(CommandStart())
async def bot_start_no_state(message: types.Message):
    user_id = message.from_user.id
    user = await select_client(user_id)
    if not user:
        await create_client(username=message.from_user.username, telegram_id=user_id)
        await message.answer("\n".join(
            [
                f'Вы добалены в базу данных'
            ]
        ))
    else:
        await message.answer("\n".join(
            [
                f'Вы уже есть в базе данных'
            ]
        ))
