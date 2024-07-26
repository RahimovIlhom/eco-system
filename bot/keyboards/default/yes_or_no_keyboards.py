from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def yes_or_no(lang: str = 'uz') -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    yes_button = KeyboardButton(
        text="👍 Ha" if lang == 'uz' else "👍 Да"
    )
    no_button = KeyboardButton(
        text="🙅 Yo'q" if lang == 'uz' else "🙅 Нет"
    )
    keyboard.add(yes_button, no_button)
    return keyboard.as_markup(resize_keyboard=True)
