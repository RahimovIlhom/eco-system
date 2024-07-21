from uuid import uuid4

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InputFile, FSInputFile

from loader import dp, db
from filters import ChatTypeFilter, EmployeeFilter
from keyboards.inline import choose_game_manu, CreateQRCodeCallbackData
from keyboards.default import employee_menu
from utils import create_qr_poster


@dp.message(ChatTypeFilter('private'), EmployeeFilter(), lambda msg: msg.text in ['📱 QR code chiqarish', '📱 Вывод QR-кода'])
async def qr_code_handler(message: Message):
    lang = 'uz' if message.text == '📱 QR code chiqarish' else 'ru'
    TEXTS = {
        'uz': {
            "accept": "QR code chiqarish uchun konkursni tanlang:",
            "reject": "❌ QR code chiqarish hozirda mumkin emas!"
        },
        'ru': {
            'accept': "Выберите конкурс для генерации QR-кода:",
            'reject': "❌ Генерация QR кода в настоящее время невозможна!"
        }
    }
    games = await db.get_active_games()
    if not games:
        await message.answer(TEXTS[lang]['reject'])
    else:
        await message.answer(TEXTS[lang]['accept'], reply_markup=await choose_game_manu(lang))


@dp.callback_query(EmployeeFilter(), CreateQRCodeCallbackData.filter())
async def create_qr_code(call: CallbackQuery, callback_data: CreateQRCodeCallbackData):
    employee = await db.get_employee(call.from_user.id)
    lang = employee['language']
    game_id = callback_data.game_id
    employee = await db.get_employee(call.from_user.id)
    eco_branch_id = employee['eco_branch_id']
    code = f"{uuid4()}".split('-')[0]
    while await db.check_qr_code(code):
        code = f"{uuid4()}".split('-')[0]

    await db.add_qr_code(game_id, eco_branch_id, code)
    TEXTS = {
        'uz': {
            "text": "Aktivlik vaqti",
        },
        'ru': {
            "text": "Время активности",
        }
    }
    qr_path = await create_qr_poster(code, text=TEXTS[lang]['text'])
    await call.message.delete()

    photo = FSInputFile(qr_path)

    # Send the photo
    try:
        await call.message.answer_photo(photo, reply_markup=await employee_menu(lang))
    except TelegramBadRequest as err:
        await call.message.answer(f"{err}", reply_markup=await employee_menu(lang))

