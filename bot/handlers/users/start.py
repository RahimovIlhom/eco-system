from aiogram import types
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message
from aiogram.utils.payload import decode_payload

from loader import dp, db
from keyboards.default import language_markup, admin_menu, employee_menu, participant_menu
from filters import ChatTypeFilter, AdminFilter, EmployeeFilter
from .register import register_qr_code, register_user
from states import AddParticipantStates


@dp.message(ChatTypeFilter('private'), CommandStart(), AdminFilter())
async def admin_start(message: types.Message, state: FSMContext):
    await state.clear()
    admin_lang = await db.admin_get_language(message.from_user.id)
    if not admin_lang:
        await message.answer(f"Iltimos, tilni tanlang / Пожалуйста, выберите язык.",
                             reply_markup=await language_markup())
        await state.set_state(State('admin_lang'))
    else:
        TEXTS = {
            'uz': "Admin panel",
            'ru': "Панель администратора",
        }
        await message.answer(TEXTS[admin_lang['language']], reply_markup=await admin_menu(admin_lang['language']))


@dp.message(ChatTypeFilter('private'), CommandStart(), EmployeeFilter())
async def employee_start(message: types.Message, state: FSMContext):
    await state.clear()
    employee = await db.get_employee(message.from_user.id)
    lang = employee['language']
    TEXTS = {
        'uz': "Bosh menu",
        'ru': "Главное меню",
    }
    await message.answer(TEXTS[lang], reply_markup=await employee_menu(lang))


@dp.message(ChatTypeFilter('private'), CommandStart(deep_link=True))
async def participant_start_link(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()
    args = command.args
    try:
        code = ''
        payload = decode_payload(args)
    except UnicodeDecodeError:
        code = args
        payload = ''
    user = await db.get_participant(message.from_user.id)

    if user:
        await handle_existing_user(message, state, user, code)
    else:
        await handle_new_user(message, state, code, payload)


@dp.message(ChatTypeFilter('private'), CommandStart())
async def participant_start(message: types.Message, state: FSMContext):
    await state.clear()
    user = await db.get_participant(message.from_user.id)
    if user:
        await send_main_menu(message, user['language'])
    else:
        await state.set_state(AddParticipantStates.language)
        await register_user(message, state)


async def handle_existing_user(message: Message, state: FSMContext, user: dict, code: str = ''):
    if code:
        await state.set_state(State('register_qr_code'))
        await state.update_data(code=code)
        await register_qr_code(message, state, user['language'])
    else:
        await send_main_menu(message, user['language'])


async def handle_new_user(message: Message, state: FSMContext, code: str = '', payload: str = ''):
    await state.set_state(AddParticipantStates.language)
    if code:
        await state.update_data(code=code)
    elif payload:
        await state.update_data(payload=payload)
    await register_user(message, state)


async def send_main_menu(message: Message, language: str):
    TEXTS = {
        'uz': "Bosh menu",
        'ru': "Главное меню",
    }
    await message.answer(TEXTS[language], reply_markup=await participant_menu(language))


# ------------ admin set language ----------------------------------------------------------------------------------


@dp.message(State('admin_lang'), AdminFilter(), lambda msg: msg.text in ['🇺🇿 O\'zbek tili', '🇷🇺 Русский язык'])
async def set_admin_language(msg: Message, state: FSMContext):
    lang = 'uz' if msg.text == "🇺🇿 O\'zbek tili" else 'ru'
    await db.admin_set_language(msg.from_user.id, lang)
    TEXTS = {
        'uz': "Admin panel",
        'ru': "Панель администратора",
    }
    await msg.answer(TEXTS[lang], reply_markup=await admin_menu(lang))
    await state.clear()


@dp.message(State(None), AdminFilter(), lambda msg: msg.text in ['🌐 Tilni o\'zgartirish', '🌐 Изменить язык'])
async def answer_choose_language(msg: Message, state: FSMContext):
    await msg.answer("Tilni tanlang / Выберите язык", reply_markup=await language_markup())
    await state.set_state(State('admin_lang'))

# ------------ admin set language end -----------------------------------------------------------------------------


# ------------ employee set language ------------------------------------------------------------------------------


@dp.message(State('employee_lang'), EmployeeFilter(), lambda msg: msg.text in ['🇺🇿 O\'zbek tili', '🇷🇺 Русский язык'])
async def set_employee_language(msg: Message, state: FSMContext):
    lang = 'uz' if msg.text == "🇺🇿 O\'zbek tili" else 'ru'
    await db.employee_set_language(msg.from_user.id, lang)
    TEXTS = {
        'uz': "Bosh menu",
        'ru': "Главное меню",
    }
    await msg.answer(TEXTS[lang], reply_markup=await employee_menu(lang))
    await state.clear()


@dp.message(State(None), EmployeeFilter(), lambda msg: msg.text in ['🌐 Tilni o\'zgartirish', '🌐 Изменить язык'])
async def answer_choose_language(msg: Message, state: FSMContext):
    await msg.answer("Tilni tanlang / Выберите язык", reply_markup=await language_markup())
    await state.set_state(State('employee_lang'))

# ------------ employee set language end --------------------------------------------------------------------------
















