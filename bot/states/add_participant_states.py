from aiogram.fsm.state import State, StatesGroup


class AddParticipantStates(StatesGroup):
    language = State()
    save_request = State()
    phone = State()
    fullname = State()
