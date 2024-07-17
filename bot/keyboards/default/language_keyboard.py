from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardButton


async def language_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardBuilder()
    uz_button = KeyboardButton(text="🇺🇿 O'zbek tili")
    ru_button = KeyboardButton(text="🇷🇺 Русский язык")
    markup.add(uz_button, ru_button)
    return markup.as_markup(resize_keyboard=True, one_time_keyboard=True)
