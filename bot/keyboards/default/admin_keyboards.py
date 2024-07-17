from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def admin_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🏆 Konkurs bo'limi" if lang == 'uz' else "🏆 Конкурсы"),
            ],
            [
                KeyboardButton(text="🏢 Punktlar bo'limi" if lang == 'uz' else "🏢 Раздел пунктов"),
                KeyboardButton(text="👤 Xodimlari bo'limi" if lang == 'uz' else "👤 Раздел сотрудников"),
            ],
            [
                KeyboardButton(text="🌐 Tilni o'zgartirish" if lang == 'uz' else "🌐 Изменить язык")
            ],
        ],
        resize_keyboard=True
    )
    return keyboard
