from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def location_markup(lang: str = 'uz') -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    location_button = KeyboardButton(
        text="📍 Joylashuvni yuborish" if lang == 'uz' else "📍 Отправить местоположение",
        request_location=True
    )
    keyboard.add(location_button)
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)
