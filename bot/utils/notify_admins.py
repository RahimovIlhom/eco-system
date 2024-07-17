import logging

from aiogram.exceptions import TelegramBadRequest
from data.config import ADMINS


async def on_startup_notify():
    from loader import bot
    for admin in ADMINS:
        try:
            await bot.send_message(admin, "Bot ishga tushdi")

        except TelegramBadRequest as err:
            logging.exception(err)
