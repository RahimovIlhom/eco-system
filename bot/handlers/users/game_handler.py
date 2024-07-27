from aiogram.types import Message

from filters import ChatTypeFilter, AdminFilter
from loader import dp, db
from keyboards.inline import game_list_markup, GameCallbackData, game_detail_markup


@dp.message(ChatTypeFilter('private'), AdminFilter(), lambda msg: msg.text in ["🏆 Konkurslar", "🏆 Конкурсы"])
async def game_list_panel(message: Message):
    lang = 'uz' if message.text == "🏆 Konkurslar" else 'ru'
    await message.answer(message.text, reply_markup=await game_list_markup(lang))


@dp.callback_query(ChatTypeFilter('private'), GameCallbackData.filter())
async def game_panel(call: Message, callback_data: GameCallbackData):
    step = callback_data.step
    game_id = callback_data.game_id
    lang = callback_data.lang
    action = callback_data.action
    if step == -1:
        await call.message.delete()
    elif step == 0:
        await show_games(call, lang)
    elif step == 1:
        await show_game(call, game_id, lang)
    elif step == 2:
        if action == 'activate':
            await activate_game_func(call, game_id, lang)
        elif action == 'complete':
            await complete_game_func(call, game_id, lang)
        elif action == 'delete':
            await delete_game_func(call, game_id, lang)
        elif action == 'cancel':
            await cancel_game_func(call, game_id, lang)


async def show_games(call, lang):
    TEXTS = {
        'uz': '🏆 Konkurslar',
        'ru': '🏆 Конкурсы'
    }
    await call.message.edit_text(TEXTS[lang], reply_markup=await game_list_markup(lang))


async def show_game(call, game_id, lang):
    game_info = await db.get_game(game_id)

    if lang == 'uz':
        name = game_info['name_uz']
        description = game_info['description_uz']
        status = game_info['status']
        start_date = game_info['start_date']
        end_date = game_info['end_date']
    else:
        name = game_info['name_ru']
        description = game_info['description_ru']
        status = game_info['status']
        start_date = game_info['start_date']
        end_date = game_info['end_date']

    status_dict = {
        'pending': '⏳ Kutilmoqda' if lang == 'uz' else '⏳ В ожидании',
        'active': '✅ Faol' if lang == 'uz' else '✅ Активный',
        'completed': '🏁 Yakunlangan' if lang == 'uz' else '🏁 Завершено',
        'deleted': '🗑 O\'chirilgan' if lang == 'uz' else '🗑 Удалено',
        'canceled': '🚫 Bekor qilingan' if lang == 'uz' else '🚫 Отменено'
    }

    status_text = status_dict.get(status, status)

    response_text = (
        f"🆔 ID: {game_info['id']}\n"
        f"📛 {'Nomi' if lang == 'uz' else 'Название'}: {name}\n"
        f"📃 {'Tavsif' if lang == 'uz' else 'Описание'}: {description}\n"
        f"🗓 {'Boshlanish sanasi' if lang == 'uz' else 'Дата начала'}: {start_date}\n"
        f"🏁 {'Tugash sanasi' if lang == 'uz' else 'Дата окончания'}: {end_date}\n"
        f"ℹ️ {'Holat' if lang == 'uz' else 'Статус'}: {status_text}"
    )

    await call.message.edit_text(response_text, reply_markup=await game_detail_markup(game_id, lang, status))


async def activate_game_func(call, game_id, lang):
    await db.update_game_status(game_id, 'active')
    await show_game(call, game_id, lang)


async def complete_game_func(call, game_id, lang):
    await db.update_game_status(game_id, 'completed')
    await show_game(call, game_id, lang)


async def delete_game_func(call, game_id, lang):
    await db.update_game_status(game_id, 'deleted')
    await show_game(call, game_id, lang)


async def cancel_game_func(call, game_id, lang):
    await db.update_game_status(game_id, 'canceled')
    await show_game(call, game_id, lang)
