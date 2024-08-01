import asyncio

from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from filters import ChatTypeFilter, AdminFilter
from loader import dp, db
from states import AddGameInfoStates
from keyboards.default import games_menu
from utils import send_telegraph_file


@dp.message(ChatTypeFilter('private'), AdminFilter(),
            lambda msg: msg.text in ["ℹ️ Konkurs haqida ma'lumot kiritish", "ℹ️ Ввести информацию о конкурсе"])
async def add_game_info(message: Message, state: FSMContext):
    lang = 'uz' if message.text == "ℹ️ Konkurs haqida ma'lumot kiritish" else 'ru'
    TEXTS = {
        'uz': "🏆 Konkurs haqida ma'lumot <b>Sarlavhasini</b> 🇺🇿 o'zbek tilida yuboring!",
        'ru': "🏆 Отправьте информацию о конкурсе с <b>заголовком</b> на 🇺🇿 узбекском языке!",
    }
    await message.answer(TEXTS[lang], reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddGameInfoStates.title_uz)
    await state.update_data(language=lang)


# Title uzbek
@dp.message(ChatTypeFilter('private'), AdminFilter(), AddGameInfoStates.title_uz, lambda msg: msg.content_type == ContentType.TEXT)
async def add_game_info_title_uz(message: Message, state: FSMContext):
    title_uz = message.text
    await state.update_data(title_uz=title_uz)
    data = await state.get_data()
    lang = data.get('language', 'uz')
    TEXTS = {
        'uz': "🏆 Konkurs haqida ma'lumot <b>Sarlavhasini</b> 🇷🇺 rus tilida yuboring!",
        'ru': "🏆 Отправьте информацию о конкурсе с <b>заголовком</b> на 🇷🇺 русском языке!",
    }
    await message.answer(TEXTS[lang])
    await state.set_state(AddGameInfoStates.title_ru)


# Title rus
@dp.message(ChatTypeFilter('private'), AdminFilter(), AddGameInfoStates.title_ru, lambda msg: msg.content_type == ContentType.TEXT)
async def add_game_info_title_ru(message: Message, state: FSMContext):
    title_ru = message.text
    await state.update_data(title_ru=title_ru)
    data = await state.get_data()
    lang = data.get('language', 'uz')
    TEXTS = {
        'uz': "ℹ️ Konkurs haqida ma'lumot <b>Ta'rifini</b> o'zbek tilida yuboring!",
        'ru': "ℹ️ Отправьте описание конкурса на 🇺🇿 узбекском языке!",
    }
    await message.answer(TEXTS[lang])
    await state.set_state(AddGameInfoStates.description_uz)


# Description uzbek
@dp.message(ChatTypeFilter('private'), AdminFilter(), AddGameInfoStates.description_uz, lambda msg: msg.content_type == ContentType.TEXT)
async def add_game_info_description_uz(message: Message, state: FSMContext):
    description_uz = message.text
    await state.update_data(description_uz=description_uz)
    data = await state.get_data()
    lang = data.get('language', 'uz')
    TEXTS = {
        'uz': "ℹ️ Konkurs haqida ma'lumot <b>Ta'rifini</b> rus tilida yuboring!",
        'ru': "ℹ️ Отправьте описание конкурса на 🇷🇺 русском языке!",
    }
    await message.answer(TEXTS[lang])
    await state.set_state(AddGameInfoStates.description_ru)


# Description rus
@dp.message(ChatTypeFilter('private'), AdminFilter(), AddGameInfoStates.description_ru, lambda msg: msg.content_type == ContentType.TEXT)
async def add_game_info_description_ru(message: Message, state: FSMContext):
    description_ru = message.text
    await state.update_data(description_ru=description_ru)
    data = await state.get_data()
    lang = data.get('language', 'uz')
    TEXTS = {
        'uz': "🖼 Konkurs haqida ma'lumot <b>Rasmini</b> yuboring!",
        'ru': "🖼 Отправьте <b>изображение</b> конкурса!"
    }
    await message.answer(TEXTS[lang])
    await state.set_state(AddGameInfoStates.image_url)


# Image URL
@dp.message(ChatTypeFilter('private'), AdminFilter(), AddGameInfoStates.image_url, lambda msg: msg.content_type == ContentType.PHOTO)
async def add_game_info_image_url(message: Message, state: FSMContext):
    image = message.photo[-1]
    image_url = await send_telegraph_file(image)
    await state.update_data(image_url=image_url)
    # Ma'lumotlarni tayyorlash va saqlash
    data = await state.get_data()
    lang = data.get('language', 'uz')
    # Ma'lumotlarni saqlash yoki boshqa jarayonlar
    await db.add_game_infos(**data)
    await message.answer("✅ Ma'lumot muvaffaqiyatli saqlandi!" if lang == 'uz' else "✅ Информация успешно добавлена!", reply_markup=await games_menu(lang))
    await state.clear()


# Error handling for title uzbek
@dp.message(ChatTypeFilter('private'), AdminFilter(), AddGameInfoStates.title_uz, lambda msg: msg.content_type == ContentType.ANY)
async def err_add_game_info_title_uz(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    lang = data.get('language', 'uz')
    TEXTS = {
        'uz': "❗️ Iltimos, Konkurs haqida ma'lumot <b>Sarlavhasini</b> yuboring!",
        'ru': "❗️ Пожалуйста, отправьте информацию о конкурсе с <b>заголовком</b>!",
    }
    err_msg = await message.answer(TEXTS[lang])
    await asyncio.sleep(2)
    await err_msg.delete()


# Error handling for title rus
@dp.message(ChatTypeFilter('private'), AdminFilter(), AddGameInfoStates.title_ru, lambda msg: msg.content_type == ContentType.ANY)
async def err_add_game_info_title_ru(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    lang = data.get('language', 'uz')
    TEXTS = {
        'uz': "❗️ Iltimos, Konkurs haqida ma'lumot <b>Sarlavhasini</b> yuboring!",
        'ru': "❗️ Пожалуйста, отправьте описание конкурса с <b>заголовком</b>!",
    }
    err_msg = await message.answer(TEXTS[lang])
    await asyncio.sleep(2)
    await err_msg.delete()


# Error handling for description uzbek
@dp.message(ChatTypeFilter('private'), AdminFilter(), AddGameInfoStates.description_uz, lambda msg: msg.content_type == ContentType.ANY)
async def err_add_game_info_description_uz(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    lang = data.get('language', 'uz')
    TEXTS = {
        'uz': "❗️ Iltimos, Konkurs haqida ma'lumot <b>Ta'rifini</b> yuboring!",
        'ru': "❗️ Пожалуйста, отправьте описание конкурса на 🇺🇿 узбекском языке!",
    }
    err_msg = await message.answer(TEXTS[lang])
    await asyncio.sleep(2)
    await err_msg.delete()


# Error handling for description rus
@dp.message(ChatTypeFilter('private'), AdminFilter(), AddGameInfoStates.description_ru, lambda msg: msg.content_type == ContentType.ANY)
async def err_add_game_info_description_ru(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    lang = data.get('language', 'uz')
    TEXTS = {
        'uz': "❗️ Iltimos, Konkurs haqida ma'lumot <b>Ta'rifini</b> yuboring!",
        'ru': "❗️ Пожалуйста, отправьте описание конкурса на 🇷🇺 русском языке!",
    }
    err_msg = await message.answer(TEXTS[lang])
    await asyncio.sleep(2)
    await err_msg.delete()
