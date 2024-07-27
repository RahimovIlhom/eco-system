import asyncio

from aiogram.enums import ContentType
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardRemove

from loader import dp, db
from filters import ChatTypeFilter, AdminFilter
from keyboards.default import employees_menu, eco_branches_menu, games_menu
from keyboards.inline import show_eco_branches, EcoBranchesCallbackData
from states import AddEmployeeStates, AddBranchStates, AddGameStates


# ----------------------- Employee panel ---------------------------------------------------------------------

@dp.message(ChatTypeFilter('private'), AdminFilter(), State(None), lambda msg: msg.text in ["👤 Раздел сотрудников", "👤 Xodimlar bo'limi"])
async def employee_panel(message: Message):
    lang = 'ru' if message.text == "👤 Раздел сотрудников" else 'uz'
    await message.answer(message.text, reply_markup=await employees_menu(lang))


@dp.message(ChatTypeFilter('private'), AdminFilter(), lambda msg: msg.text in ["👤 Xodimlar", "👤 Сотрудники"])
async def employee_list_panel(message: Message):
    pass


@dp.message(ChatTypeFilter('private'), AdminFilter(), State(None), lambda msg: msg.text in ["➕ Xodim qo'shish", "➕ Добавить сотрудника"])
async def add_employee(message: Message, state: FSMContext):
    lang = 'uz' if message.text == "➕ Xodim qo'shish" else 'ru'
    TEXTS = {
        'uz': "Xodimning ism-familiyasini yuboring:",
        'ru': "Введите имя и фамилию вашего сотрудника:",
    }
    await message.answer(TEXTS[lang], reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddEmployeeStates.fullname)
    await state.set_data({'language': lang})


@dp.message(ChatTypeFilter('private'), AdminFilter(), AddEmployeeStates.fullname, lambda msg: msg.content_type == ContentType.TEXT)
async def add_employee_fullname(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['language']
    fullname = message.text
    await state.update_data(fullname=fullname)
    TEXTS = {
        'uz': "Xodimning telegram kontaktini yuboring:",
        'ru': "Отправьте контакт сотрудника в Telegram:",
    }
    await message.answer(TEXTS[lang])
    await state.set_state(AddEmployeeStates.contact)


@dp.message(ChatTypeFilter('private'), AdminFilter(), AddEmployeeStates.fullname, lambda msg: msg.content_type == ContentType.ANY)
async def err_add_employee_fullname(message: Message):
    await message.delete()
    data = await message.get_data()
    lang = data['language']
    TEXTS = {
        'uz': "❗️ Iltimos, xodim ism-familiyasini yuboring!",
        'ru': "❗️ Пожалуйста, отправьте имя и фамилию сотрудника!"
    }
    err_msg = await message.answer(TEXTS[lang])
    await asyncio.sleep(2)
    await err_msg.delete()


@dp.message(ChatTypeFilter('private'), AdminFilter(), AddEmployeeStates.contact, lambda msg: msg.content_type == ContentType.CONTACT)
async def add_employee_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['language']
    phone = message.contact.phone_number
    tg_id = message.contact.user_id
    TEXTS = {
        'uz': {
            'next': "Xodim punktini tanlang:",
            'already': ("❗️ Bu telegram kontakti allaqachon xodim sifatida roʻyxatdan oʻtgan!\nBoshqa kontaktni "
                        "yuboring:")
        },
        'ru': {
            'next': "Выберите отдел сотрудника:",
            'already': "❗️ Этот телеграм-контакт уже зарегистрирован как сотрудник!\nОтправьте другой контакт: "
        }
    }
    if await db.get_employee(tg_id):
        return await message.answer(TEXTS[lang]['already'])
    await state.update_data(phone=phone, tg_id=tg_id)
    await message.answer(TEXTS[lang]['next'], reply_markup=await show_eco_branches(lang))
    await state.set_state(AddEmployeeStates.eco_branch)


@dp.message(ChatTypeFilter('private'), AdminFilter(), AddEmployeeStates.contact, lambda msg: msg.content_type == ContentType.ANY)
async def err_add_employee_contact(message: Message):
    await message.delete()
    data = await message.get_data()
    lang = data['language']
    TEXTS = {
        'uz': "❗️ Iltimos, xodimning telegram kontaktini yuboring!",
        'ru': "❗️ Пожалуйста, отправьте контакт сотрудника в Telegram!"
    }
    err_msg = await message.answer(TEXTS[lang])
    await asyncio.sleep(2)
    await err_msg.delete()


@dp.callback_query(ChatTypeFilter('private'), AdminFilter(), AddEmployeeStates.eco_branch, EcoBranchesCallbackData.filter())
async def end_add_employee(call: CallbackData, callback_data: EcoBranchesCallbackData, state: FSMContext):
    data = await state.get_data()
    lang = data['language']
    data.update({'eco_branch_id': callback_data.branch_id})
    TEXTS = {
        'uz': {
            'success': "✅ Xodim muvaffaqiyatli ro'yxatdan o'tkazildi!",
            'failed': "❗️ Xodim ro'yxatdan o'tishda xatolik yuz berdi!",
            'end': "👤 Xodimlar bo'limi"
        },
        'ru': {
            'success': "✅ Сотрудник успешно зарегистрирован!",
            'failed': "❗️ Произошла ошибка при регистрации сотрудника!",
            'end': "👤 Раздел сотрудников"
        }
    }
    await state.clear()
    try:
        await db.add_employee(**data)  # TODO: add_employee() -> add_employee
    except Exception as e:
        await call.message.edit_text(TEXTS[lang]['failed'] + f"\n\nerror: {e}", reply_markup=None)
    else:
        await call.message.edit_text(TEXTS[lang]['success'], reply_markup=None)
    finally:
        await call.message.answer(TEXTS[lang]['end'], reply_markup=await employees_menu(lang))


@dp.message(ChatTypeFilter('private'), AdminFilter(), AddEmployeeStates.eco_branch, lambda msg: msg.content_type == ContentType.ANY)
async def err_add_employee_branch(message: Message):
    await message.delete()
    data = await message.get_data()
    lang = data['language']
    TEXTS = {
        'uz': "❗️ Iltimos, punktni tanlang!",
        'ru': "❗️ Пожалуйста, выберите пункт!"
    }
    err_msg = await message.answer(TEXTS[lang])
    await asyncio.sleep(2)
    await err_msg.delete()

# ------------------------- End employee panel ---------------------------------------------------------------

# ------------------------- EcoBranch panel ------------------------------------------------------------------


@dp.message(ChatTypeFilter('private'), AdminFilter(), lambda msg: msg.text in ["🏢 Punktlar bo'limi", "🏢 Раздел пунктов"])
async def eco_branch_panel(message: Message):
    lang = 'ru' if message.text == "🏢 Раздел пунктов" else 'uz'
    await message.answer(message.text, reply_markup=await eco_branches_menu(lang))


@dp.message(ChatTypeFilter('private'), AdminFilter(), lambda msg: msg.text in ["🏢 Punktlar", "🏢 Пункты"])
async def eco_branch_list_panel(message: Message):
    pass


@dp.message(ChatTypeFilter('private'), AdminFilter(), lambda msg: msg.text in ["➕ Punkt qo'shish", "➕ Добавить пункт"])
async def add_eco_branch(message: Message, state: FSMContext):
    lang = 'ru' if message.text == "➕ Добавить пункт" else 'uz'
    TEXTS = {
        'uz': "🇺🇿 Punkt nomini o'zbek tilida yuboring:",
        'ru': "🇺🇿 Отправьте название пункта на узбекском языке:"
    }
    await message.answer(TEXTS[lang], reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddBranchStates.name_uz)
    await state.set_data({'language': lang})


@dp.message(ChatTypeFilter('private'), AdminFilter(), AddBranchStates.name_uz, lambda msg: msg.content_type == ContentType.TEXT)
async def add_eco_branch_name(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['language']
    name = message.text
    await state.update_data(name_uz=name)
    TEXTS = {
        'uz': "🇷🇺 Punkt nomini rus tilida yuboring:",
        'ru': "🇷🇺 Отправьте название пункта на русском языке:"
    }
    await message.answer(TEXTS[lang])
    await state.set_state(AddBranchStates.name_ru)


@dp.message(ChatTypeFilter('private'), AdminFilter(), AddBranchStates.name_uz, lambda msg: msg.content_type == ContentType.ANY)
async def err_add_eco_branch_name(message: Message):
    await message.delete()
    data = await message.get_data()
    lang = data['language']
    TEXTS = {
        'uz': "❗️ Iltimos, punktni nomini yuboring!",
        'ru': "❗️ Пожалуйста, отправьте название пункта!"
    }
    err_msg = await message.answer(TEXTS[lang])
    await asyncio.sleep(2)
    await err_msg.delete()


@dp.message(ChatTypeFilter('private'), AdminFilter(), AddBranchStates.name_ru, lambda msg: msg.content_type == ContentType.TEXT)
async def add_eco_branch_name(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data['language']
    name = message.text
    await state.update_data(name_ru=name)
    TEXTS = {
        'uz': "📍 Punkt lokatsiyasini yuboring:",
        'ru': "📍 Отправьте местоположение пункта:"
    }
    await message.answer(TEXTS[lang])
    await state.set_state(AddBranchStates.location)


@dp.message(ChatTypeFilter('private'), AdminFilter(), AddBranchStates.name_ru, lambda msg: msg.content_type == ContentType.ANY)
async def err_add_eco_branch_name(message: Message):
    await message.delete()
    data = await message.get_data()
    lang = data['language']
    TEXTS = {
        'uz': "❗️ Iltimos, punktni nomini yuboring!",
        'ru': "❗️ Пожалуйста, отправьте название пункта!"
    }
    err_msg = await message.answer(TEXTS[lang])
    await asyncio.sleep(2)
    await err_msg.delete()


@dp.message(ChatTypeFilter('private'), AdminFilter(), AddBranchStates.location, lambda msg: msg.content_type == ContentType.LOCATION)
async def add_eco_branch_location(message: Message, state: FSMContext):
    location = message.location
    await state.update_data(location=location)
    data = await state.get_data()
    lang = data['language']
    TEXTS = {
        'uz': {
            'success': "✅ Punkt muvaffaqiyatli ro'yxatdan o'tkazildi!",
            'failed': "❗️ Punkt ro'yxatdan o'tishda xatolik yuz berdi!",
            'end': "🏢 Punktlar bo'limi"
        },
        'ru': {
            'success': "✅ Пункт успешно зарегистрирован!",
            'failed': "❗️ Произошла ошибка при регистрации пункта!",
            'end': "🏢 Раздел пунктов"
        }
    }
    try:
        await db.add_branch(**data)  # TODO: add_branch() -> add_eco_branch
    except Exception as e:
        await message.answer(TEXTS[lang]['failed'] + f"\n\nerror: {e}", reply_markup=None)
    else:
        await message.answer(TEXTS[lang]['success'], reply_markup=None)
    await message.answer(TEXTS[lang]['end'], reply_markup=await eco_branches_menu(lang))
    await state.clear()


@dp.message(ChatTypeFilter('private'), AdminFilter(), AddBranchStates.location, lambda msg: msg.content_type == ContentType.ANY)
async def err_add_eco_branch_location(message: Message):
    await message.delete()
    data = await message.get_data()
    lang = data['language']
    TEXTS = {
        'uz': "❗️ Iltimos, punkt lokatsiyasini yuboring!",
        'ru': "❗️ Пожалуйста, отправьте местоположение пункта!"
    }
    err_msg = await message.answer(TEXTS[lang])
    await asyncio.sleep(2)
    await err_msg.delete()

# ------------------------- end EcoBranch panel -----------------------------------------------------------

# ------------------------- start Game panel --------------------------------------------------------------


@dp.message(ChatTypeFilter('private'), AdminFilter(), lambda msg: msg.text in ["🏆 Konkurs bo'limi", "🏆 Раздел конкурсов"])
async def game_panel(message: Message):
    lang = 'uz' if message.text == "🏆 Konkurs bo'limi" else 'ru'
    await message.answer(message.text, reply_markup=await games_menu(lang))


@dp.message(ChatTypeFilter('private'), AdminFilter(), lambda msg: msg.text in ["➕ Konkurs qo'shish", "➕ Добавить конкурс"])
async def game_panel(message: Message, state: FSMContext):
    lang = 'uz' if message.text == "➕ Konkurs qo'shish" else 'ru'
    TEXTS = {
        'uz': "🇺🇿 Konkurs o'zbek tilida yuboring:",
        'ru': "🇺🇿 Конкурс отправьте на узбекском языке:"
    }
    await message.answer(TEXTS[lang], reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddGameStates.name_uz)
    await state.set_data({'language': lang})


@dp.message(ChatTypeFilter('private'), AdminFilter(), AddGameStates.name_uz, lambda msg: msg.content_type == ContentType.TEXT)
async def add_game_name_uz(message: Message, state: FSMContext):
    game_name = message.text
    await state.update_data(game_name_uz=game_name)
    data = await state.get_data()
    lang = data['language']
    TEXTS = {
        'uz': "🇷🇺 Konkurs rus tilida yuboring:",
        'ru': "🇷🇺 Отправьте конкурс на русском языке:"
    }
    await message.answer(TEXTS[lang])
    await state.set_state(AddGameStates.name_ru)


@dp.message(ChatTypeFilter('private'), AdminFilter(), AddGameStates.name_uz, lambda msg: msg.content_type == ContentType.ANY)
async def err_add_game_name_uz(message: Message):
    await message.delete()
    data = await message.get_data()
    lang = data['language']
    TEXTS = {
        'uz': "❗️ Iltimos, konkurs nomini o'zbek tilida yuboring!",
        'ru': "❗️ Пожалуйста, отправьте название конкурса на узбекском языке!"
    }
    err_msg = await message.answer(TEXTS[lang])
    await asyncio.sleep(2)
    await err_msg.delete()


@dp.message(ChatTypeFilter('private'), AdminFilter(), AddGameStates.name_ru, lambda msg: msg.content_type == ContentType.TEXT)
async def add_game_name(message: Message, state: FSMContext):
    game_name = message.text
    await state.update_data(game_name_ru=game_name)
    data = await state.get_data()
    lang = data['language']
    TEXTS = {
        'uz': {
            'success': "✅ Konkurs muvaffaqiyatli qo'shildi!",
            'failed': "❗️ Konkurs qo'shishda xatolik yuz berdi!",
            'end': "🏆 Konkurslar bo'limi"
        },
        'ru': {
            'success': "✅ Конкурс успешно добавлен!",
            'failed': "❗️ Произошла ошибка при добавлении конкурса!",
            'end': "🏆 Раздел конкурсов"
        }
    }
    try:
        await db.add_game(**data)  # TODO: add_game() -> add_eco_game
    except Exception as e:
        await message.answer(TEXTS[lang]['failed'] + f"\n\nerror: {e}", reply_markup=None)
    else:
        await message.answer(TEXTS[lang]['success'], reply_markup=None)
    await message.answer(TEXTS[lang]['end'], reply_markup=await games_menu(lang))
    await state.clear()


@dp.message(ChatTypeFilter('private'), AdminFilter(), AddGameStates.name_ru, lambda msg: msg.content_type == ContentType.ANY)
async def err_add_game_name_ru(message: Message):
    await message.delete()
    data = await message.get_data()
    lang = data['language']
    TEXTS = {
        'uz': "❗️ Iltimos, konkurs nomini rus tilida yuboring!",
        'ru': "❗️ Пожалуйста, отправьте название конкурса на русском языке!"
    }
    err_msg = await message.answer(TEXTS[lang])
    await asyncio.sleep(2)
    await err_msg.delete()

# ------------------------- end Game panel ----------------------------------------------------------------




















