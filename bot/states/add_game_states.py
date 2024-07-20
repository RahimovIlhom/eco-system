from aiogram.fsm.state import State, StatesGroup


class AddGameStates(StatesGroup):
    name = State()
