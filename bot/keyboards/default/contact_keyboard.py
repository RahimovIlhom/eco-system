from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def contact_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📞 Kontaktni yuborish" if lang == 'uz' else "📞 Отправить контакт", request_contact=True),
            ],
        ],
        resize_keyboard=True
    )
    return keyboard
