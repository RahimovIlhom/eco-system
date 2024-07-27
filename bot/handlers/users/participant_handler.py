from datetime import timedelta, datetime

from aiogram.enums import ContentType
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.deep_linking import create_start_link

from loader import dp, db, bot
from filters import ChatTypeFilter
from states import RegisterQRCodeStates
from keyboards.default import participant_menu, location_markup, setting_markup, language_markup, information_markup


# ----------------------- Start register QR code---------------------------------------------------------
@dp.message(ChatTypeFilter('private'), State(None), lambda msg: msg.text in ["📱 QR kodni ro'yxatdan o'tkazish", "📱 Зарегистрировать QR-код"])
async def register_qr_code_for_code(message: Message, state: FSMContext):
    lang = 'uz' if message.text == "📱 QR kodni ro'yxatdan o'tkazish" else 'ru'
    TEXTS = {
        'uz': "🔡 Rasmdagi kodni yuboring",
        'ru': "🔡 Отправьте код с картинки"
    }
    await message.answer(TEXTS[lang], reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegisterQRCodeStates.code)
    await state.set_data({'language': lang})


@dp.message(ChatTypeFilter('private'), RegisterQRCodeStates.code, lambda msg: msg.content_type == ContentType.TEXT)
async def register_qr_code(message: Message, state: FSMContext):
    code = message.text.lower()
    data = await state.get_data()
    lang = data['language']
    TEXTS = {
        'uz': {
            'already_registered': "Bu QR kod avval {fullname} tomonidan ro'yxatdan o'tkazilgan",
            'success': "Joylashuvingizni quyidagi tugma orqali yuboring:\n\n",
            'expiration_time': "Bu QR kod aktivlik vaqti tugagan.",
            'no_active': "Bu QR kod aktiv emas",
            'not_found': "Bu QR kod topilmadi"
        },
        'ru': {
            'already_registered': "Этот QR-код уже был зарегистрирован {fullname}",
            'success': "Отправьте ваше местоположение через кнопку ниже:\n\n",
            'expiration_time': "Этот QR-код истек по времени активности.",
            'no_active': "Этот QR-код неактивен.",
            'not_found': "Этот QR-код не найден"
        }
    }
    qr_code = await db.check_qr_code(code)

    if qr_code:
        if qr_code['is_active']:
            expiration_time = qr_code['created_at'] + timedelta(minutes=qr_code['activity_time'])
            if expiration_time >= datetime.now():
                if await db.get_registered_qr_code(qr_code['id']):
                    await db.update_active_qr_code(qr_code['id'])
                    await message.answer(TEXTS[lang]['already_registered'].format(fullname=qr_code['fullname']),
                                         reply_markup=await participant_menu(lang))
                    await state.clear()
                else:
                    await message.answer(TEXTS[lang]['success'], reply_markup=await location_markup(lang))
                    await state.set_state(State('qr_code_location'))
                    await state.update_data(qr_code_id=qr_code['id'], eco_branch_id=qr_code['eco_branch_id'],
                                            language=lang)
            else:
                await db.update_active_qr_code(qr_code['id'])
                await message.answer(TEXTS[lang]['expiration_time'],
                                     reply_markup=await participant_menu(lang))
                await state.clear()
        else:
            await message.answer(TEXTS[lang]['no_active'],
                                 reply_markup=await participant_menu(lang))
            await state.clear()
    else:
        await message.answer(TEXTS[lang]['not_found'], reply_markup=await participant_menu(lang))
        await state.clear()


# ----------------------- Start settings menu---------------------------------------------------------

@dp.message(ChatTypeFilter('private'), State(None), lambda msg: msg.text in ["⚙️ Sozlamalar", "⚙️ Настройки"])
async def settings_menu(message: Message):
    lang = 'uz' if message.text == "⚙️ Sozlamalar" else 'ru'
    await message.answer(message.text, reply_markup=await setting_markup(lang))


@dp.message(ChatTypeFilter('private'), State(None), lambda msg: msg.text in ["🌐 Tilni o'zgartirish", "🌐 Изменить язык"])
async def change_language(message: Message, state: FSMContext):
    lang = 'uz' if message.text == "🌐 Tilni o'zgartirish" else 'ru'
    TEXTS = {
        'uz': "Tilni tanlang",
        'ru': "Выберите язык"
    }
    await message.answer(TEXTS[lang], reply_markup=await language_markup())
    await state.set_state(State('participant_lang'))


@dp.message(State('participant_lang'), lambda msg: msg.text in ['🇺🇿 O\'zbek tili', '🇷🇺 Русский язык'])
async def set_participant_language(msg: Message, state: FSMContext):
    lang = 'uz' if msg.text == "🇺🇿 O\'zbek tili" else 'ru'
    await db.participant_set_language(msg.from_user.id, lang)
    TEXTS = {
        'uz': "Bosh menu",
        'ru': "Главное меню",
    }
    await msg.answer(TEXTS[lang], reply_markup=await participant_menu(lang))
    await state.clear()


# ----------------------- Start information menu---------------------------------------------------------

@dp.message(ChatTypeFilter('private'), State(None), lambda msg: msg.text in ["ℹ️ Ma'lumotlarim", "ℹ️ Мои данные"])
async def information_handler(message: Message):
    lang = 'uz' if message.text == "ℹ️ Ma'lumotlarim" else 'ru'
    await message.answer(message.text, reply_markup=await information_markup(lang))


# ----------------------- Start about concurs menu---------------------------------------------------------


@dp.message(ChatTypeFilter('private'), State(None), lambda msg: msg.text in ["🏆 Konkurs haqida", "🏆 О конкурсе"])
async def about_concurs(message: Message):
    lang = 'uz' if message.text == "🏆 Konkurs haqida" else 'ru'
    info = await db.get_game_info()

    if info:
        if lang == 'uz':
            formatted_message = (
                f"🏆 <b>Konkurs Haqida</b>\n\n"
                f"<b>{info['title_uz']}</b>\n\n"
                f"<b>Tavsifi:</b> {info['description_uz']}\n"
            )
        else:
            formatted_message = (
                f"🏆 <b>О конкурсе</b>\n\n"
                f"<b>{info['title_ru']}</b>\n\n"
                f"<b>Описание:</b> {info['description_ru']}\n"
            )

        # Rasmni yuborish
        if info['image_url']:
            try:
                await message.answer_photo(info['image_url'], caption=formatted_message, parse_mode='Markdown')
            except TelegramBadRequest:
                await message.answer(formatted_message)
        else:
            await message.answer(formatted_message)
    else:
        if lang == 'uz':
            formatted_message = "❌ Konkurs haqidagi ma'lumot topilmadi."
        else:
            formatted_message = "❌ Информация о конкурсе не найдена."

        await message.answer(formatted_message)


# ---------------------------- My points menu --------------------------------------------------------

@dp.message(ChatTypeFilter('private'), State(None), lambda msg: msg.text in ["💎 Mening ballarim", "💎 Мои баллы"])
async def my_points(message: Message):
    lang = 'uz' if message.text == "💎 Mening ballarim" else 'ru'
    TEXTS = {
        'uz': "Siz {number} ta do'stingizni taklif qilgansiz.\n\n💎 Sizning ballaringiz: {points}",
        'ru': "Вы пригласили {number} друзей.\n\n💎 Ваши баллы: {points}"
    }
    result = await db.get_participant_points(message.from_user.id)
    number = result['number']
    await message.answer(TEXTS[lang].format(number=number, points=number*5))


# --------------------------- My friends menu --------------------------------------------------------

@dp.message(ChatTypeFilter('private'), State(None), lambda msg: msg.text in ["👥 Do'stlarni taklif qilish", "👥 Пригласить друзей"])
async def invite_friends(message: Message):
    lang = 'uz' if message.text == "👥 Do'stlarni taklif qilish" else 'ru'
    info = await db.get_game_info()
    link = await create_start_link(bot, f'{message.from_user.id}', encode=True)
    if info:
        if lang == 'uz':
            formatted_message = (
                f"🏆 <b>Konkurs Haqida</b>\n\n"
                f"<b>{info['title_uz']}</b>\n\n"
                f"{info['description_uz']}\n\n"
                "Konkursda ishtirok etish: <a href='{link}'>Konkursga o'tish</a>"
            )
        else:
            formatted_message = (
                f"🏆 <b>О конкурсе</b>\n\n"
                f"<b>{info['title_ru']}</b>\n\n"
                f"{info['description_ru']}\n\n"
                "Участие в конкурсе: <a href='{link}'>Перейти к конкурсу</a>"
            )
    else:
        if lang == 'uz':
            formatted_message = ("Salom, bizning 🏆 sovrunli konkursimizda qatnashishni istaysizmi?\n\n"
                                 "Unda bizga qo'shiling.\n👉 <a href='{link}'>Konkursga o'tish</a>")
        else:
            formatted_message = ("Привет, хотите принять участие в нашем 🏆 призовом конкурсе?\n\n"
                                 "Тогда присоединяйтесь к нам.\n👉 <a href='{link}'>Перейти к конкурсу</a>")
    await message.answer(formatted_message.format(link=link))
