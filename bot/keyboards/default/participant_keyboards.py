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
                KeyboardButton(text="💎 Mening ballarim" if lang == 'uz' else "💎 Мои баллы"),
                KeyboardButton(text="👥 Do'stlarni taklif qilish" if lang == 'uz' else "👥 Пригласить друзей"),
            ],
            [
                KeyboardButton(text="🏆 Konkurs haqida" if lang == 'uz' else "🏆 О конкурсе"),
            ]
        ],
        resize_keyboard=True,
    )
    return keyboard
