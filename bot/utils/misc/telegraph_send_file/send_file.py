import aiohttp
from aiogram import types
from io import BytesIO
from aiogram.types import InputFile


async def send_telegraph_file(photo: types.PhotoSize) -> str:
    from loader import bot

    # `photo.file_id` ni olish orqali faylni olish
    file = await bot.get_file(photo.file_id)

    # Faylni `BytesIO` obyektiga yuklash
    file_url = f'https://api.telegram.org/file/bot{bot.token}/{file.file_path}'
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            file_content = await response.read()

    # Faylni `BytesIO` obyektiga joylash
    file = BytesIO(file_content)
    file.seek(0)

    # `aiohttp` yordamida `telegra.ph` ga faylni yuborish
    form = aiohttp.FormData()
    form.add_field(
        name='file',
        value=file,
        content_type='multipart/form-data',
        filename='photo.jpg'  # Fayl nomi, kerakli formatda qo'ying
    )

    async with aiohttp.ClientSession() as session:
        async with session.post('https://telegra.ph/upload', data=form) as response:
            img_src = await response.json()

    # Olingan rasm manzilini qaytarish
    link = 'http://telegra.ph/' + img_src[0]["src"]
    return link
