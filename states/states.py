from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    CHANGE_FIO = State()
    CHANGE_ADDRESS = State()
    CHANGE_PHONE = State()
