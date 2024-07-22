from aiogram.fsm.state import State
from aiogram.types import Message

from loader import dp, db
from filters import ChatTypeFilter


@dp.message(ChatTypeFilter('private'), State(None), lambda msg: msg.text in ["📱 QR kodni ro'yxatdan o'tkazish", "📱 Зарегистрировать QR-код"])
async def register_qr_code_for_code(message: Message):
    pass


@dp.message(ChatTypeFilter('private'), State(None), lambda msg: msg.text in ["⚙️ Sozlamalar", "⚙️ Настройки"])
async def settings_handler(message: Message):
    pass


@dp.message(ChatTypeFilter('private'), State(None), lambda msg: msg.text in ["ℹ️ Ma'lumotlarim", "ℹ️ Мои данные"])
async def information_handler(message: Message):
    pass


@dp.message(ChatTypeFilter('private'), State(None), lambda msg: msg.text in ["🏆 Konkurs haqida", "🏆 О конкурсе"])
async def about_concurs(message: Message):
    pass
