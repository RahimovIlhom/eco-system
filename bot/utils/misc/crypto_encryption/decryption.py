from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from environs import Env

env = Env()
env.read_env()


async def decrypt_data(ciphertext: bytes) -> str:
    key = eval(env.str("CRYPTO_KEY"))
    iv = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]

    # Shifrlash obyekti yaratamiz
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Deshifrlash
    padded_data = decryptor.update(actual_ciphertext) + decryptor.finalize()

    # To'ldirishni olib tashlash
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    return data.decode()
