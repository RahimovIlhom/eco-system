from uuid import uuid4

from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from loader import dp, db
from filters import ChatTypeFilter, EmployeeFilter
from keyboards.inline import choose_game_manu, CreateQRCodeCallbackData


@dp.message(ChatTypeFilter('private'), EmployeeFilter(), lambda msg: msg.text in ['📱 QR code chiqarish', '📱 Вывод QR-кода'])
async def qr_code_handler(message: Message):
    lang = 'uz' if message.text == '📱 QR code chiqarish' else 'ru'
    TEXTS = {
        'uz': "QR code chiqarish uchun konkursni tanlang:",
        'ru': "Выберите конкурс для генерации QR-кода:"
    }
    await message.answer(TEXTS[lang], reply_markup=await choose_game_manu())


@dp.callback_query(EmployeeFilter(), CreateQRCodeCallbackData.filter())
async def create_qr_code(call: CallbackQuery, callback_data: CreateQRCodeCallbackData):  # bu funksiya yakunlanmagan
    game_id = callback_data.game_id
    employee = await db.get_employee(call.from_user.id)
    eco_branch_id = employee['eco_branch_id']
    code = f"{uuid4()}".split('-')[0]
    while await db.check_qr_code(code):
        code = f"{uuid4()}".split('-')[0]
    # create QR code image
    await db.add_qr_code(game_id, eco_branch_id, code)

