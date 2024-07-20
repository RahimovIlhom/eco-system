from aiogram.enums import ContentType
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message, ReplyKeyboardRemove

from loader import dp, db
from filters import ChatTypeFilter, AdminFilter
from keyboards.default import employees_menu
from keyboards.inline import show_eco_branches, EcoBranchesCallbackData
from states import AddEmployeeStates


# ----------------------- Employee panel ---------------------------------------------------------------------

@dp.message(ChatTypeFilter('private'), AdminFilter(), State(None), lambda msg: msg.text in ["👤 Раздел сотрудников", "👤 Xodimlar bo'limi"])
async def admin_panel(message: Message):
    lang = 'ru' if message.text == "👤 Раздел сотрудников" else 'uz'
    await message.answer(message.text, reply_markup=await employees_menu(lang))


@dp.message(ChatTypeFilter('private'), AdminFilter(), State(None), lambda msg: msg.text in ["➕ Xodim qo'shish", "➕ Добавить сотрудника"])
async def admin_panel(message: Message, state: FSMContext):
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
    await message.answer(TEXTS[lang]['next'], reply_markup=await show_eco_branches())
    await state.set_state(AddEmployeeStates.eco_branch)


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
            'success': "✅ Сотрудник был успешно зарегистрирован!",
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

# ------------------------- End employee panel ---------------------------------------------------------------

# ------------------------- EcoBranch panel ------------------------------------------------------------------



























