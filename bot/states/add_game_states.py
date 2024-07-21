from aiogram.fsm.state import State, StatesGroup


class AddGameStates(StatesGroup):
    name_uz = State()
    name_ru = State()
