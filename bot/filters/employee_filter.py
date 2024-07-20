from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from loader import db


async def get_employees_ids():
    employees = await db.get_employees()
    employees_ids = [employee['tg_id'] for employee in employees]
    return employees_ids


class EmployeeFilter(BaseFilter):
    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        return str(message.from_user.id) in await get_employees_ids()
