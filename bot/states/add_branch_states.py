from aiogram.fsm.state import State, StatesGroup


class AddBranchStates(StatesGroup):
    name = State()
    location = State()
