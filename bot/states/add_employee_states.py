from aiogram.fsm.state import State, StatesGroup


class AddEmployeeStates(StatesGroup):
    fullname = State()
    contact = State()
    eco_branch = State()
