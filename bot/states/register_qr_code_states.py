from aiogram.fsm.state import State, StatesGroup


class RegisterQRCodeStates(StatesGroup):
    code = State()
