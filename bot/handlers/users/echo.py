from aiogram import types
from aiogram.fsm.state import State

from loader import dp

from bot.filters import ChatTypeFilter


# Echo bot
@dp.message(ChatTypeFilter(['private']), State(None))
async def bot_echo(message: types.Message):
    if message.text:  # Xabar matni bo'sh emasligini tekshirish
        await message.answer(message.text)
    else:
        await message.answer("Xabar matni bo'sh!")
