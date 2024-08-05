from datetime import datetime

from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from loader import dp, db
from keyboards.default import participant_menu
from filters import ChatTypeFilter

from utils.misc.crypto_encryption import decrypt_data


@dp.callback_query(lambda call: call.data == 'agree')
async def add_card_func(call: CallbackQuery, state: FSMContext):
    tg_id = call.from_user.id
    participant = await db.get_participant(tg_id)
    lang = participant.get('language', 'uz')
    TEXTS = {
        'uz': "💳 Karta raqamingizni yuboring.\n\nMisol uchun: 8600 0000 0000 0000",
        'ru': "💳 Отправьте номер вашей карты.\n\nНапример: 8600 0000 0000 0000"
    }

    await call.message.delete()
    await call.message.answer(TEXTS[lang], reply_markup=ReplyKeyboardRemove())
    await state.set_state(State('add_card'))
    await state.update_data(lang=lang)


async def get_card_type(card_number):
    uzcard_prefixes = ["8600", "5614"]
    humo_prefixes = ["9860"]

    card_prefix = card_number[:4]

    if card_prefix in uzcard_prefixes:
        return "uzcard"
    elif card_prefix in humo_prefixes:
        return "humo"
    else:
        return False


@dp.message(State('add_card'), lambda msg: msg.content_type == ContentType.TEXT)
async def add_card_func(message: Message, state: FSMContext):
    TEXTS = {
        'uz': {
            'success': "✅ Karta qo'shildi",
            'error': "❗️ Karta raqamini to'g'ri kiriting",
            'not_card': "Bunday karta raqamni qo'sha olmaysiz! Uzcard yoki Humo kartasini qo'shishingiz mumkin."
        },
        'ru': {
            'success': "✅ Карта добавлена",
            'error': "❗️ Введите правильный номер карты",
            'not_card': "Вы не можете добавить такую карту! Можно добавить только карты Uzcard или Humo."
        }
    }
    data = await state.get_data()
    lang = data['lang']

    card = message.text.replace(' ', '').replace('-', '').replace('_', '').replace('.', '')
    if len(card) != 16 or not card.isdigit():
        await message.answer(TEXTS[lang]['error'])
        return
    card_type = await get_card_type(card)
    if card_type is False:
        await message.answer(TEXTS[lang]['not_card'])
        return

    await db.add_plastic_card(tg_id=message.from_user.id, card_type=card_type, card_number=card)

    await message.answer(TEXTS[lang]['success'], reply_markup=await participant_menu(lang))
    await state.clear()


@dp.callback_query(lambda call: call.data == 'disagree')
async def not_add_card_func(call: CallbackQuery):
    participant = await db.get_participant(call.from_user.id)
    lang = participant.get('language', 'uz')
    TEXTS = {
        'uz': ("⚠️ Siz karta ma'lumotingizni yubormagansiz!\n\nMukofotni olish uchun quyidagi tugmani bosing, "
               "imkoniyatni qo'ldan boy bermang."),
        'ru': ("⚠️ Вы не отправили информацию о своей карте!\n\nНажмите на кнопку ниже, чтобы получить приз, "
               "не упустите шанс.")
    }

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Kartam ma'lumotlarini yuborishga roziman"
                    if lang == 'uz' else "Я согласен отправить данные моей карты",
                    callback_data="agree"
                )
            ]
        ]
    )

    await call.message.edit_text(TEXTS[lang], reply_markup=keyboard)


def format_card_number(card_number):
    return ' '.join(card_number[i:i + 4] for i in range(0, len(card_number), 4))


def format_date(date_str):
    if isinstance(date_str, str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
    elif isinstance(date_str, datetime):
        date_obj = date_str
    else:
        raise ValueError("date_str must be a str or datetime object")
    return date_obj.strftime("%H:%M, %d-%m-%Y")


@dp.message(ChatTypeFilter('private'), lambda msg: msg.text in ["💳 Mening kartam", "💳 Мои карты"])
async def get_card_number_func(message: Message):
    lang = 'uz' if message.text == '💳 Mening kartam' else 'ru'
    TEXTS = {
        'uz': ("💳 <b>Karta turi:</b> {card_type}\n🔢 <b>Karta raqami:</b> {card_number}\n📅 <b>Karta qo'shilgan "
               "sana:</b> {created_at}"),
        'ru': ("💳 <b>Тип карты:</b> {card_type}\n🔢 <b>Номер карты:</b> {card_number}\n📅 <b>Дата добавления "
               "карты:</b> {created_at}")
    }
    plastic_card = await db.get_plastic_card(tg_id=message.from_user.id)
    if plastic_card:
        formatted_card_number = format_card_number(await decrypt_data(plastic_card['card_number']))
        formatted_date = format_date(plastic_card['created_at'])
        response_message = TEXTS[lang].format(
            card_type=plastic_card['card_type'],
            card_number=formatted_card_number,
            created_at=formatted_date
        )
        remove_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🚫 Kartani o'chirish" if lang == 'uz' else "🚫 Удалить карту",
                        callback_data='remove_card'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔒 Yopish" if lang == 'uz' else "🔒 Закрыть",
                        callback_data='close'
                    )
                ]
            ]
        )
    else:
        response_message = "❗️ Karta ma'lumotlari topilmadi." if lang == 'uz' else "❗️ Данные карты не найдены."
        remove_keyboard = None

    await message.answer(response_message, parse_mode="HTML", reply_markup=remove_keyboard)


@dp.callback_query(lambda call: call.data == 'remove_card')
async def confirm_remove_card(call: CallbackQuery):
    participant = await db.get_participant(call.from_user.id)
    lang = participant.get('language', 'uz')
    TEXTS = {
        'uz': "❗️ Siz rostdan ham kartani o'chirmoqchimisiz?",
        'ru': "❗️ Вы хотите удалить свою карту?"
    }
    confirm_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ Ha" if lang == 'uz' else "❌ Да", callback_data='confirm_remove'),
                InlineKeyboardButton(text="✅ Yo'q" if lang == 'uz' else "✅ Нет", callback_data='cancel_remove')
            ]
        ]
    )
    await call.message.edit_text(TEXTS[lang], reply_markup=confirm_keyboard)


@dp.callback_query(lambda call: call.data == 'confirm_remove')
async def remove_card_func(call: CallbackQuery):
    participant = await db.get_participant(call.from_user.id)
    lang = participant.get('language', 'uz')
    await db.remove_plastic_card(tg_id=call.from_user.id)
    await call.message.edit_text("Karta o'chirildi." if lang == 'uz' else "Карта удалена.")


@dp.callback_query(lambda call: call.data == 'cancel_remove')
async def cancel_remove_func(call: CallbackQuery):
    participant = await db.get_participant(call.from_user.id)
    lang = participant.get('language', 'uz')
    await call.message.edit_text("Karta o'chirish bekor qilindi." if lang == 'uz' else "Карта удаление отменено.")


@dp.callback_query(lambda call: call.data == 'close')
async def close_func(call: CallbackQuery):
    await call.message.delete()
