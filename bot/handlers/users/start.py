from aiogram import types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message

from loader import dp, db
from keyboards.default import language_markup, admin_menu
from filters import ChatTypeFilter, AdminFilter, EmployeeFilter


@dp.message(ChatTypeFilter('private'), CommandStart(), AdminFilter())
async def admin_start(message: types.Message, state: FSMContext):
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
        await message.answer(TEXTS[admin_lang[0]], reply_markup=await admin_menu(admin_lang[0]))


@dp.message(ChatTypeFilter('private'), CommandStart())
async def bot_start(message: Message):
    await message.answer(f"Assalomu alaykum, hurmatli {message.from_user.full_name} EcoSystem botiga xush kelibsiz!\n"
                         f"Здравствуйте, уважаемый {message.from_user.full_name}, добро пожаловать в EcoSystem бот!\n\n"
                         f"Iltimos, tilni tanlang / Пожалуйста, выберите язык.", reply_markup=await language_markup())


# ------------ admin set language ----------------------------------------------------------------------------------


@dp.message(State('admin_lang'), lambda msg: msg.text in ['🇺🇿 O\'zbek tili', '🇷🇺 Русский язык'], AdminFilter())
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
















