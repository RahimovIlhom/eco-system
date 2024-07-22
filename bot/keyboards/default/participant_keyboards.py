from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


async def participant_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📱 QR kodni ro'yxatdan o'tkazish" if lang == 'uz' else "📱 Зарегистрировать QR-код")
            ],
            [
                KeyboardButton(text="⚙️ Sozlamalar" if lang == 'uz' else "⚙️ Настройки"),
                KeyboardButton(text="ℹ️ Ma'lumotlarim" if lang == 'uz' else "ℹ️ Мои данные"),
            ],
            [
                KeyboardButton(text="🏆 Konkurs haqida" if lang == 'uz' else "🏆 О конкурсе"),
            ]
        ],
        resize_keyboard=True,
    )
    return keyboard
