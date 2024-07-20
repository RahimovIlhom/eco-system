from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from loader import db


class CreateQRCodeCallbackData(CallbackData, prefix="eco_branch"):
    game_id: int


async def make_qr_code_callback_data(game_id: int) -> str:
    return CreateQRCodeCallbackData(game_id=game_id).pack()


async def choose_game_manu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    games = await db.get_active_games()
    for game in games:
        keyboard.add(
            InlineKeyboardButton(
                text=game['name'],
                callback_data=await make_qr_code_callback_data(game_id=game['id'])
            )
        )
    keyboard.adjust(1)
    return keyboard.as_markup()
