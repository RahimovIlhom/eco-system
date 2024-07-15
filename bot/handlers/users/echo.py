from aiogram import types
from aiogram.fsm.state import State

from loader import dp


# Echo bot
@dp.message(State())
async def bot_echo(message: types.Message):
    await message.answer(message.text)
