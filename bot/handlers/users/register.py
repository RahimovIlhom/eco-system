from datetime import timedelta, datetime

from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.default import language_markup, contact_keyboard, participant_menu, location_markup, yes_or_no
from pymysql import IntegrityError
from states import AddParticipantStates
from loader import dp, db
from filters import ChatTypeFilter
from utils import get_distance


# ----------------------- Start register QR code---------------------------------------------------------

async def register_qr_code(message, state, lang):
    data = await state.get_data()
    code = data.get('code', None)
    qr_code = await db.check_qr_code(code)
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


@dp.message(ChatTypeFilter('private'), State('qr_code_location'), lambda msg: msg.content_type == ContentType.LOCATION)
async def add_qr_code_location(message: Message, state: FSMContext):
    location = message.location
    data = await state.get_data()
    lang = data['language']
    qr_code_id = data['qr_code_id']
    eco_branch_id = data['eco_branch_id']
    TEXTS = {
        'uz': {
            'success': "✅ QR kod muvaffaqiyatli ro'yxatdan o'tkazildi!\n\n",
            'error': "❗️ Xatolik yuz berdi!\n\n",
            'distance': ("Ushbu QR kod {distance} m masofada yuborilgan. QR kodni roʻyxatdan oʻtkazish uchun uni kod "
                         "olgan joydan 10 m masofada yuboring.\n\n")
        },
        'ru': {
            'success': "✅ QR-код успешно зарегистрирован!\n\n",
            'error': "❗️ Произошла ошибка!\n\n",
            'distance': ("Этот QR-код был отправлен на расстоянии {distance} м. Чтобы зарегистрировать QR-код, "
                         "отправьте его на расстоянии не более 10 м от места получения кода.\n\n")
        }
    }
    eco_branch_dict = await db.get_eco_branch(eco_branch_id)
    distance = get_distance((location.latitude, location.longitude),
                            (eco_branch_dict['latitude'], eco_branch_dict['longitude']))
    if distance > 10:
        await message.answer(TEXTS[lang]['distance'].format(distance=distance),
                             reply_markup=await participant_menu(lang))
        await state.clear()
        return
    await db.add_location(location)  # TODO: Add location to db
    location_dict = await db.get_location_by_coordinates(location)
    await db.update_active_qr_code(qr_code_id)
    try:
        await db.add_registered_qrcode(participant_id=message.from_user.id, qrcode_id=qr_code_id,
                                       location_id=location_dict['id'])
    except IntegrityError as err:
        await message.answer(TEXTS[lang]['error'] + f"error: {err}", reply_markup=await participant_menu(lang))
        await state.clear()
        return
    await message.answer(TEXTS[lang]['success'], reply_markup=await participant_menu(lang))
    await state.clear()


#  ------------------------------ End register QR code ----------------------------------------------

# ----------------------------- Start add participant -----------------------------------------------


async def register_user(message, state):
    await message.answer(f"Assalomu alaykum, hurmatli {message.from_user.full_name} EcoSystem botiga xush kelibsiz!\n"
                         f"Здравствуйте, уважаемый {message.from_user.full_name}, добро пожаловать в EcoSystem бот!\n\n"
                         f"Iltimos, tilni tanlang / Пожалуйста, выберите язык.", reply_markup=await language_markup())


@dp.message(ChatTypeFilter('private'), AddParticipantStates.language,
            lambda msg: msg.text in ["🇺🇿 O'zbek tili", '🇷🇺 Русский язык'])
async def add_language(message: Message, state: FSMContext):
    lang = 'uz' if message.text == "🇺🇿 O'zbek tili" else 'ru'
    await state.update_data(language=lang)
    TEXTS = {
        'uz': "Ma'lumotlaringizni saqlashimizga rozilik bildirasizmi?\n\n⚠️ Eslatma!\nKonkursda qatnashish uchun rozilik bildiring.",
        'ru': "Согласны ли вы на хранение ваших данных?\n\n⚠️ Напоминание!\nПожалуйста, дайте согласие для участия в конкурсе."
    }
    await message.answer(TEXTS[lang], reply_markup=await yes_or_no(lang))
    await state.set_state(AddParticipantStates.save_request)


@dp.message(ChatTypeFilter('private'), AddParticipantStates.save_request,
            lambda msg: msg.text in ["👍 Ha", "👍 Да", "🙅 Yo'q", "🙅 Нет"])
async def question_save_request(message: Message, state: FSMContext):
    lang = 'uz' if message.text in ["👍 Ha", "🙅 Yo'q"] else 'ru'
    TEXTS = {
        'uz': "📞 Quyidagi tugmani bosib, kontaktingizni yuboring",
        'ru': "📞 Нажмите на кнопку ниже, чтобы отправить ваш контакт"
    }
    if message.text in ["🙅 Yo'q", "🙅 Нет"]:
        ERR_TEXTS = {
            'uz': "❗️ Kechirasiz siz konkursimizda ishtirok eta olmaysiz!",
            'ru': "❗️ Извините, вы не можете участвовать в нашем конкурсе!"
        }
        await message.answer(ERR_TEXTS[lang], reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return
    await message.answer(TEXTS[lang], reply_markup=await contact_keyboard(lang))
    await state.set_state(AddParticipantStates.phone)


@dp.message(ChatTypeFilter('private'), AddParticipantStates.phone, lambda msg: msg.content_type == ContentType.CONTACT)
async def add_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['language']
    TEXTS = {
        'uz': "Ism-familiyangizni yuboring",
        'ru': "Отправьте ваше имя и фамилию"
    }
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    await message.answer(TEXTS[lang], reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddParticipantStates.fullname)


@dp.message(ChatTypeFilter('private'), AddParticipantStates.fullname, lambda msg: msg.content_type == ContentType.TEXT)
async def add_fullname(message: Message, state: FSMContext):
    fullname = message.text
    await state.update_data(fullname=fullname)
    data = await state.get_data()
    lang = data['language']
    code = data.get('code', None)
    data.update({'tg_id': message.from_user.id})
    TEXTS = {
        'uz': {
            'added': "👍 Hurmatli {fullname} siz muvaffaqiyatli ro'yxatdan o'tdingiz!\n\n",
            'error': ("❗️ Roʻyxatdan oʻtishda xatolik yuz berdi! Qayta roʻyxatdan oʻtish uchun /start buyrugʻini "
                      "yuboring.\n\n")
        },
        'ru': {
            'added': "👍 Уважаемый {fullname}, вы успешно зарегистрировались!\n\n",
            'error': ("❗️ Произошла ошибка при регистрации! Отправьте команду /start заново, "
                      "чтобы зарегистрироваться.\n\n")
        }
    }
    try:
        await db.add_participant(**data)
    except Exception as e:
        await message.answer(TEXTS[lang]['error'] + f"error: {e}")
        await state.clear()
    else:
        await message.answer(TEXTS[lang]['added'].format(fullname=fullname))
        if code:
            await register_qr_code(message, state, lang)
        else:
            TEXTS = {
                'uz': "Bosh menu",
                'ru': "Главное меню",
            }
            await message.answer(TEXTS[lang], reply_markup=await participant_menu(lang))
        await state.clear()

# ----------------------------- End add participant -------------------------------------------------
