from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
from environs import Env

env = Env()
env.read_env()


# Shifrlash uchun funksiyalar
async def encrypt_data(plaintext: str) -> bytes:
    key = eval(env.str("CRYPTO_KEY"))
    # Kalit 256-bit bo'lishi kerak (32 bayt)
    if len(key) != 32:
        raise ValueError("Kalit uzunligi 32 bayt bo'lishi kerak (256-bit)")

    # Tasodifiy IV (Initialization Vector) generatsiya qilamiz
    iv = os.urandom(16)

    # Shifrlash obyekti yaratamiz
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Ma'lumotlarni to'ldirish
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    # Shifrlash
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext
