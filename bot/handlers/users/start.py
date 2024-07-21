from aiogram import types
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message
from aiogram.utils.payload import decode_payload

from loader import dp, db
from keyboards.default import language_markup, admin_menu, employee_menu
from filters import ChatTypeFilter, AdminFilter, EmployeeFilter


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
async def employee_start(message: types.Message):
    employee = await db.get_employee(message.from_user.id)
    lang = employee['language']
    TEXTS = {
        'uz': "Bosh menu",
        'ru': "Главное меню",
    }
    await message.answer(TEXTS[lang], reply_markup=await employee_menu(lang))


@dp.message(ChatTypeFilter('private'), CommandStart(deep_link=True))
async def bot_start(message: Message, command: CommandObject):
    args = command.args
    print(args)
    payload = decode_payload(args)
    print(payload)
    await message.answer(f"Assalomu alaykum, hurmatli {message.from_user.full_name} EcoSystem botiga xush kelibsiz!\n"
                         f"Здравствуйте, уважаемый {message.from_user.full_name}, добро пожаловать в EcoSystem бот!\n\n"
                         f"Iltimos, tilni tanlang / Пожалуйста, выберите язык.", reply_markup=await language_markup())


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
















