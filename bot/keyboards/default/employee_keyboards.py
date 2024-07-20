from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


async def employee_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📱 QR code chiqarish" if lang == 'uz' else "📱 Вывод QR-кода")
            ],
            [
                KeyboardButton(text="🌐 Tilni o'zgartirish" if lang == 'uz' else "🌐 Изменить язык"),
            ]
        ],
        resize_keyboard=True,
    )
    return keyboard
