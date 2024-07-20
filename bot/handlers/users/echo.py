from aiogram import types
from aiogram.fsm.state import State

from loader import dp
from filters import ChatTypeFilter, AdminFilter
from keyboards.default import admin_menu


# Echo bot
@dp.message(ChatTypeFilter(['private']), State(None), AdminFilter())
async def bot_echo(message: types.Message):
    if message.text:
        if message.text in ['🔙 Orqaga', '🔙 Назад']:
            lang = 'uz' if message.text == "🔙 Orqaga" else 'ru'
            await message.answer("Admin panel" if lang == 'uz' else "Главное меню", reply_markup=await admin_menu(lang))
        else:
            await message.answer(message.text)
    else:
        await message.answer("Xabar matni bo'sh!")


# Echo bot
@dp.message(ChatTypeFilter(['private']), State(None))
async def bot_echo(message: types.Message):
    if message.text:  # Xabar matni bo'sh emasligini tekshirish
        await message.answer(message.text)
    else:
        await message.answer("Xabar matni bo'sh!")
