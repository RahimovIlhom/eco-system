from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import db


class GameCallbackData(CallbackData, prefix="game"):
    game_id: int
    step: int
    lang: str
    action: str


async def make_qr_code_callback_data(game_id: int, step: int, lang: str = 'uz', action: str = '') -> str:
    return GameCallbackData(game_id=game_id, step=step, lang=lang, action=action).pack()


async def game_list_markup(lang: str = 'uz') -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 0
    keyboard = InlineKeyboardBuilder()
    games = await db.get_games()
    for game in games:
        STATUS = {
            'uz': {
                'pending': '⏳ Kutilmoqda',
                'active': '✅ Faol',
                'completed': '🏁 Yakunlangan',
                'deleted': '🗑 O\'chirilgan',
                'canceled': '🚫 Bekor qilindi',
            },
            'ru': {
                'pending': '⏳ В ожидании',
                'active': '✅ Активный',
                'completed': '🏁 Завершено',
                'deleted': '🗑 Удалено',
                'canceled': '🚫 Отменено',
            }
        }
        keyboard.add(
            InlineKeyboardButton(
                text=game['name_uz'] + f": {STATUS[lang].get(game['status'], 'No status')}" if lang == 'uz' else game['name_ru'],
                callback_data=await make_qr_code_callback_data(game_id=game['id'], step=CURRENT_LEVEL+1, lang=lang)
            )
        )
    keyboard.add(InlineKeyboardButton(
        text='❌ Oynani yopish' if lang == 'uz' else '❌ Закрыть окно',
        callback_data=await make_qr_code_callback_data(game_id=0, step=CURRENT_LEVEL-1, lang=lang)
    ))
    keyboard.adjust(1)
    return keyboard.as_markup()


async def game_detail_markup(game_id: int, lang: str = 'uz', status: str = 'pending') -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 1
    keyboard = InlineKeyboardBuilder()
    active_button = InlineKeyboardButton(
        text='✅ Faollashtirish' if lang == 'uz' else '✅ Активировать',
        callback_data=await make_qr_code_callback_data(game_id=game_id, step=CURRENT_LEVEL+1, lang=lang, action='activate')
    )
    finish_button = InlineKeyboardButton(
            text='🏁 Yakunlash' if lang == 'uz' else '🏁 Завершить',
            callback_data=await make_qr_code_callback_data(game_id=game_id, step=CURRENT_LEVEL+1, lang=lang, action='complete')
        )
    delete_button = InlineKeyboardButton(
        text='🗑 O\'chirish' if lang == 'uz' else '🗑 Удалить',
        callback_data=await make_qr_code_callback_data(game_id=game_id, step=CURRENT_LEVEL+1, lang=lang, action='delete')
    )
    cancel_button = InlineKeyboardButton(
        text='❌ Bekor qilish' if lang == 'uz' else '❌ Отменить',
        callback_data=await make_qr_code_callback_data(game_id=game_id, step=CURRENT_LEVEL+1, lang=lang, action='cancel')
    )
    if status == 'pending':
        keyboard.row(delete_button, active_button, cancel_button)
    elif status == 'active':
        keyboard.row(finish_button)
    keyboard.row(
        InlineKeyboardButton(
            text='◀️ Orqaga' if lang == 'uz' else '◀️ Назад',
            callback_data=await make_qr_code_callback_data(game_id=game_id, step=CURRENT_LEVEL-1, lang=lang)
        )
    )
    keyboard.adjust(2)
    return keyboard.as_markup()
