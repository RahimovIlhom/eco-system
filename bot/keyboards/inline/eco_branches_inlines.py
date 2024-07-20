from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


class EcoBranchesCallbackData(CallbackData, prefix="eco_branch"):
    branch_id: int


async def create_eco_callback_data(branch_id: int) -> str:
    return EcoBranchesCallbackData(branch_id=branch_id).pack()


async def show_eco_branches() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    branches = await db.get_branches()
    for branch in branches:
        keyboard.add(
            InlineKeyboardButton(
                text=branch['name'],
                callback_data=await create_eco_callback_data(branch_id=branch['id'])
            )
        )
    keyboard.adjust(1)
    return keyboard.as_markup()
