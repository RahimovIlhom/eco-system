from aiogram import types

from loader import dp
from keyboards.default import location_markup
from filters import ChatTypeFilter
from utils import get_location_details


@dp.message(ChatTypeFilter('private'), lambda message: message.text == 'hello')
async def send_hello(msg: types.Message):
    await msg.answer("Joylashuvingizni yuboring", reply_markup=await location_markup())


@dp.message(ChatTypeFilter('private'), lambda msg: msg.content_type == types.ContentType.LOCATION)
async def handle_location(msg: types.Message):
    location = msg.location
    details = get_location_details(location.latitude, location.longitude)

    await msg.answer(f"Manzil: {details['city']}, {details['road']}, {details['house_number']}")

