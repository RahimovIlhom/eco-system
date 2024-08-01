from aiogram.fsm.state import State, StatesGroup


class AddGameInfoStates(StatesGroup):
    title_uz = State()
    title_ru = State()
    description_uz = State()
    description_ru = State()
    image_url = State()
