from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardButton


async def setting_markup(lang: str = 'uz') -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardBuilder()
    language_button = KeyboardButton(text="🌐 Tilni o'zgartirish" if lang == 'uz' else "🌐 Изменить язык")
    back_button = KeyboardButton(text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад")
    markup.row(language_button)
    markup.row(back_button)
    return markup.as_markup(resize_keyboard=True, one_time_keyboard=True)
