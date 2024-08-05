from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardRemove

from filters import ChatTypeFilter
from loader import dp, db
from keyboards.default import information_markup


# ------------------------- Start profile menu -----------------------------------------------------------

@dp.message(ChatTypeFilter('private'), State(None), lambda msg: msg.text in ["👤 Profilim", "👤 Профиль"])
async def profile(message: Message):
    lang = 'uz' if message.text == "👤 Profilim" else 'ru'
    profile_info = await db.get_participant(message.from_user.id)

    if profile_info:
        created_at = profile_info['created_at']
        formatted_created_at = created_at.strftime("%H:%M, %d-%m-%Y")

        if lang == 'uz':
            formatted_message = (
                f"<b>Ishtirokchi Ma'lumotlari</b>\n\n"
                f"🆔 <b>Telegram ID:</b> {profile_info['tg_id']}\n"
                f"🌐 <b>Til:</b> {profile_info['language']}\n"
                f"👤 <b>Ism-familiya:</b> {profile_info['fullname']}\n"
                f"📞 <b>Telefon raqami:</b> {profile_info['phone']}\n"
                f"🗓️ <b>Ro'yxatga olingan sana:</b> {formatted_created_at}\n"
            )
        else:
            formatted_message = (
                f"<b>Информация об участнике</b>\n\n"
                f"🆔 <b>Telegram ID:</b> {profile_info['tg_id']}\n"
                f"🌐 <b>Язык:</b> {profile_info['language']}\n"
                f"👤 <b>Полное имя:</b> {profile_info['fullname']}\n"
                f"📞 <b>Телефонный номер:</b> {profile_info['phone']}\n"
                f"🗓️ <b>Дата регистрации:</b> {formatted_created_at}\n"
            )
    else:
        if lang == 'uz':
            formatted_message = "❌ Ishtirokchi topilmadi."
        else:
            formatted_message = "❌ Участник не найден."

    await message.answer(formatted_message)


# ------------------------- Start set name menu -----------------------------------------------------------


@dp.message(ChatTypeFilter('private'), State(None), lambda msg: msg.text in ["✏️ Ismni o'zgartirish", "✏️ Изменить имя"])
async def settings(message: Message, state: FSMContext):
    lang = 'uz' if message.text == "✏️ Ismni o'zgartirish" else 'ru'
    TEXTS = {
        'uz': "Ism-familiyangizni yuboring",
        'ru': "Отправьте ваше полное имя"
    }
    await message.answer(TEXTS[lang], reply_markup=ReplyKeyboardRemove())
    await state.set_state(State('edit_name'))
    await state.set_data({'language': lang})


@dp.message(State('edit_name'), lambda msg: msg.content_type == ContentType.TEXT)
async def edit_name(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['language']
    TEXTS = {
        'uz': "✅ Ism-familiyangiz o'zgartirildi",
        'ru': "✅ Ваше полное имя изменено"
    }
    await db.participant_set_fullname(message.from_user.id, message.text)
    await message.answer(TEXTS[lang], reply_markup=await information_markup(lang))
    await state.clear()


# ------------------------- Start QR codes menu -----------------------------------------------------------


@dp.message(ChatTypeFilter('private'), State(None), lambda msg: msg.text in ["🗂 QR kodlarim", "🗂 Мои QR-коды"])
async def register_qr_codes_info(message: Message, state: FSMContext):
    lang = 'uz' if message.text == "🗂 QR kodlarim" else 'ru'
    qr_codes = await db.get_participant_qr_codes(message.from_user.id)

    if qr_codes:
        if lang == 'uz':
            formatted_message = "📋 <b>Sizning QR kodlaringiz</b>\n\nUmumiy soni: " + str(len(qr_codes)) + "\n\n"
            for qr in qr_codes:
                created_at = qr['created_at'].strftime("%H:%M, %d-%m-%Y")
                formatted_message += (
                    f"🆔 <b>QR kod:</b> {qr['code'].upper()}\n"
                    f"🗓️ <b>Ro'yxatga olingan sana:</b> {created_at}\n\n"
                )
        else:
            formatted_message = "📋 <b>Ваши QR-коды</b>\n\nВсего: " + str(len(qr_codes)) + "\n\n"
            for qr in qr_codes:
                created_at = qr['created_at'].strftime("%H:%M, %d-%m-%Y")
                formatted_message += (
                    f"🆔 <b>QR код:</b> {qr['code'].upper()}\n"
                    f"🗓️ <b>Дата регистрации:</b> {created_at}\n\n"
                )
    else:
        if lang == 'uz':
            formatted_message = "❌ Sizning QR kodlaringiz topilmadi."
        else:
            formatted_message = "❌ Ваши QR-коды не найдены."

    await message.answer(formatted_message)
