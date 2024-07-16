from aiogram import types
from aiogram.filters import CommandStart

from loader import dp

from keyboards.default import language_markup
from filters import ChatTypeFilter


@dp.message(ChatTypeFilter('private'), CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Assalomu alaykum, hurmatli {message.from_user.full_name} EcoSystem botiga xush kelibsiz!\n"
                         f"Здравствуйте, уважаемый {message.from_user.full_name}, добро пожаловать в EcoSystem бот!\n\n"
                         f"Iltimos, tilni tanlang / Пожалуйста, выберите язык.", reply_markup=await language_markup())
