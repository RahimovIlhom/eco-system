from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from data.config import ADMINS


class AdminFilter(BaseFilter):
    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        return message.from_user.id in ADMINS
