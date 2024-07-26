from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


async def information_markup(lang: str = 'uz') -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="👤 Profilim" if lang == 'uz' else "👤 Профиль"),
                KeyboardButton(text="✏️ Ismni o'zgartirish" if lang == 'uz' else "✏️ Изменить имя"),
            ],
            [
                KeyboardButton(text="🗂 QR kodlarim" if lang == 'uz' else "🗂 Мои QR-коды"),
            ],
            [
                KeyboardButton(text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад"),
            ]
        ],
        resize_keyboard=True,
    )
    return keyboard
