import asyncio
import os

from PIL import Image, ImageDraw, ImageFont
import qrcode
from datetime import datetime, timedelta

from aiogram.utils.deep_linking import create_start_link


async def create_qr_poster(unique_code, text='Aktivlik vaqti', validity_minutes=5):
    from loader import bot
    template_path = 'data/qr_template/qrcode.png'
    link = await create_start_link(bot, f"{unique_code}")
    bot_link = link.split('?')[0]
    # QR kodni yaratish
    qr = qrcode.QRCode(version=5, box_size=10, border=5)
    qr.add_data(link)
    qr.make(fit=True)
    qr_img = qr.make_image(fill='black', back_color='white')

    # Asosiy rasmni ochish
    base_img = Image.open(template_path)

    # QR kodni mos joyga joylashtirish
    qr_img = qr_img.resize((650, 650))  # QR kodning o'lchamini moslashtiring
    base_img.paste(qr_img, (380, 800))  # Mos joyga joylashtirish (x, y)

    # Rasmga matn qo'shish
    draw = ImageDraw.Draw(base_img)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 25)

    # QR kod yaratilgan vaqti va aktivlik tugash vaqti
    created_at = datetime.now()
    expires_at = created_at + timedelta(minutes=validity_minutes)  # Aktivlik muddati
    created_text = f"{text}: {created_at.strftime('%H:%M:%S')}"
    expires_text = f"> {expires_at.strftime('%H:%M:%S, %d-%m-%Y')}"
    if text == "Aktivlik vaqti":
        draw.text((350, 635), created_text, fill="black", font=font)
        draw.text((690, 635), expires_text, fill="black", font=font)
    else:
        draw.text((320, 635), created_text, fill="black", font=font)
        draw.text((740, 635), expires_text, fill="black", font=font)

    # Unikal kod
    draw.text((570, 1600), f"Code: {str(unique_code).upper()}", fill="black", font=font)

    # SSILKA
    draw.text((450, 1900), bot_link, fill="black", font=font)

    # Natijani saqlash
    file_path = "data/qr_codes/"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    output_path = f"{file_path}{unique_code}.png"
    base_img.save(output_path)

    return output_path


# unique_code = "ABC123XYZ"  # Unikal kod
# asyncio.run(create_qr_poster(unique_code,))
