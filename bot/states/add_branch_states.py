from aiogram.fsm.state import State, StatesGroup


class AddBranchStates(StatesGroup):
    name_uz = State()
    name_ru = State()
    chief_name = State()
    phone = State()
    location = State()
