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
                f"👤 **Ishtirokchi Ma'lumotlari**\n"
                f"🆔 **Telegram ID:** {profile_info['tg_id']}\n"
                f"🌐 **Til:** {profile_info['language']}\n"
                f"📛 **Ism-familiya:** {profile_info['fullname']}\n"
                f"📞 **Telefon raqami:** {profile_info['phone']}\n"
                f"🗓️ **Ro'yxatga olingan sana:** {formatted_created_at}\n"
            )
        else:
            formatted_message = (
                f"👤 **Информация об участнике**\n"
                f"🆔 **Telegram ID:** {profile_info['tg_id']}\n"
                f"🌐 **Язык:** {profile_info['language']}\n"
                f"📛 **Полное имя:** {profile_info['fullname']}\n"
                f"📞 **Телефонный номер:** {profile_info['phone']}\n"
                f"🗓️ **Дата регистрации:** {formatted_created_at}\n"
            )
    else:
        if lang == 'uz':
            formatted_message = "❌ Ishtirokchi topilmadi."
        else:
            formatted_message = "❌ Участник не найден."

    await message.answer(formatted_message, parse_mode='Markdown')


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
            formatted_message = "📋 **Sizning QR kodlaringiz**\n\nUmumiy soni: " + str(len(qr_codes)) + "\n\n"
            for qr in qr_codes:
                created_at = qr['created_at'].strftime("%H:%M, %d-%m-%Y")
                formatted_message += (
                    f"🆔 **QR kod:** {qr['code'].upper()}\n"
                    f"🗓️ **Ro'yxatga olingan sana:** {created_at}\n\n"
                )
        else:
            formatted_message = "📋 **Ваши QR-коды**\n\nВсего: " + str(len(qr_codes)) + "\n\n"
            for qr in qr_codes:
                created_at = qr['created_at'].strftime("%H:%M, %d-%m-%Y")
                formatted_message += (
                    f"🆔 **QR код:** {qr['code'].upper()}\n"
                    f"🗓️ **Дата регистрации:** {created_at}\n\n"
                )
    else:
        if lang == 'uz':
            formatted_message = "❌ Sizning QR kodlaringiz topilmadi."
        else:
            formatted_message = "❌ Ваши QR-коды не найдены."

    await message.answer(formatted_message, parse_mode='Markdown')
