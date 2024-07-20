from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def admin_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🏆 Konkurs bo'limi" if lang == 'uz' else "🏆 Конкурсы"),
            ],
            [
                KeyboardButton(text="🏢 Punktlar bo'limi" if lang == 'uz' else "🏢 Раздел пунктов"),
                KeyboardButton(text="👤 Xodimlar bo'limi" if lang == 'uz' else "👤 Раздел сотрудников"),
            ],
            [
                KeyboardButton(text="🌐 Tilni o'zgartirish" if lang == 'uz' else "🌐 Изменить язык")
            ],
        ],
        resize_keyboard=True
    )
    return keyboard


async def employees_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="👤 Xodimlar" if lang == 'uz' else "👤 Сотрудники"),
                KeyboardButton(text="➕ Xodim qo'shish" if lang == 'uz' else "➕ Добавить сотрудника"),
            ],
            [
                KeyboardButton(text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard
