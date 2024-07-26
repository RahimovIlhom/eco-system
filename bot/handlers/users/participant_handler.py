from datetime import timedelta, datetime

from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardRemove

from loader import dp, db
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
    pass
