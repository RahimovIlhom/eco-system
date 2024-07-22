from aiogram.fsm.state import State, StatesGroup


class AddParticipantStates(StatesGroup):
    language = State()
    phone = State()
    fullname = State()
