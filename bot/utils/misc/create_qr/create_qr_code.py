import qrcode
from PIL import Image, ImageDraw


def create_stylish_qr(data, size=300, border_color=(0, 0, 0), background_color=(255, 255, 255)):
    # QR kodni yaratish
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # Tasvir o'lchamini o'zgartirish
    img = img.resize((size, size), Image.Resampling.LANCZOS)

    # Tasvirni chiroyli qilish
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # Tasvirning fonini chiroyli qilish
    background = Image.new('RGB', (width, height), background_color)
    background.paste(img, (0, 0))

    # Chegarani chiroyli qilish
    border_thickness = 10
    border = Image.new('RGB', (width + border_thickness * 2, height + border_thickness * 2), border_color)
    border.paste(background, (border_thickness, border_thickness))

    return border


# Funksiyani chaqirish va QR kodni saqlash
stylish_qr = create_stylish_qr('https://qrplanet.com')
stylish_qr.save('stylish_qr_code.png')
stylish_qr.show()
