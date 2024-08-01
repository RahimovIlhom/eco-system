from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def admin_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🏆 Konkurs bo'limi" if lang == 'uz' else "🏆 Раздел конкурсов"),
                KeyboardButton(text="🏢 Punktlar bo'limi" if lang == 'uz' else "🏢 Раздел пунктов"),
            ],
            # [
            #     KeyboardButton(text="🏢 Punktlar bo'limi" if lang == 'uz' else "🏢 Раздел пунктов"),
            #     KeyboardButton(text="👤 Xodimlar bo'limi" if lang == 'uz' else "👤 Раздел сотрудников"),
            # ],
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


async def eco_branches_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🏢 Punktlar" if lang == 'uz' else "🏢 Пункты"),
                KeyboardButton(text="➕ Punkt qo'shish" if lang == 'uz' else "➕ Добавить пункт"),
            ],
            [
                KeyboardButton(text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


async def games_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🏆 Konkurslar" if lang == 'uz' else "🏆 Конкурсы"),
                KeyboardButton(text="➕ Konkurs qo'shish" if lang == 'uz' else "➕ Добавить конкурс"),
            ],
            [
                KeyboardButton(text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard
