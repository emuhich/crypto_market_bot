from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import InputFile
from aiogram.utils.markdown import hbold

from loader import dp, bot
from utils.db_api.db_commands import select_all_products


@dp.message_handler(Command("send_product"))
async def bot_start(message: types.Message):
    products = await select_all_products()

    for product in products:
        text = "\n".join(
            [
                f'{hbold(f"Название:")} {product.name}\n',
                f'{hbold("Описание:")}\n {product.description}\n',
                f'{hbold("Цена:")} {product.price} р.',

            ]
        )
        await bot.send_photo(photo=product.image, chat_id=message.chat.id,caption=text)

