import requests
import json
from environs import Env

env = Env()
env.read_env()

API_TOKEN = env.str('BOT_TOKEN')


def send_message(chat_id, game_name: str, lang: str = 'uz'):
    TEXTS = {
        'uz': """
Assalomu alaykum!

Tabriklaymiz, siz bizning {game_name} konkursimizning g'olibi bo'ldingiz! 🎉

Sizni g'oliblik bilan qutlaymiz va mukofotingizni olish uchun quyidagi ko'rsatmalarga amal qilishingizni so'raymiz.

Mukofotni olish uchun bizga quyidagi karta ma'lumotlarini taqdim etishingiz kerak.

Iltimos, ushbu ma'lumotlarni taqdim eting, shunda biz mukofot pulini sizning kartangizga o'tkazamiz. Mukofot puli sizning kartangizga muvaffaqiyatli o'tkazilgandan so'ng, sizga xabar beriladi.

Karta ma'lumotingizni yuborishga rozilik bildirasizmi?

Eslatmalar:

1. Mukofotni olish jarayonida biron-bir muammo yuzaga kelsa yoki qo'shimcha yordam kerak bo'lsa, biz bilan bog'laning.
2. Karta ma'lumotlarini yubormasangiz konkurs mukofotini ololmaysiz.
3. Mukofot puli faqat o'yinda ishtirok etgan odamning nomidagi kartaga o'tkaziladi.
        """,
        'ru': """
Здравствуйте!

Поздравляем, вы стали победителем нашего конкурса {game_name}! 🎉

Мы поздравляем вас с победой и просим следовать инструкциям ниже, чтобы получить свой приз.

Для получения приза вам необходимо предоставить следующие данные карты.

Пожалуйста, предоставьте эту информацию, чтобы мы могли перевести призовые деньги на вашу карту. После успешного перевода на вашу карту, вам будет отправлено уведомление.

Вы согласны предоставить информацию о своей карте?

Примечания:

1. Если возникнут какие-либо проблемы или понадобится дополнительная помощь при получении приза, свяжитесь с нами.
2. Если вы не предоставите данные карты, вы не сможете получить приз конкурса.
3. Призовые деньги будут переведены только на карту, зарегистрированную на имя участника конкурса.
        """
    }

    url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'

    inline_keyboard = {
        "inline_keyboard": [
            [
                {"text": "👍 Roziman" if lang == 'uz' else "👍 Согласен", "callback_data": "agree"},
                {"text": "👎 Rozi emasman" if lang == 'uz' else "👎 Не согласен", "callback_data": "disagree"}
            ]
        ]
    }

    payload = {
        'chat_id': chat_id,
        'text': TEXTS[lang].format(game_name=game_name),
        'reply_markup': json.dumps(inline_keyboard)
    }

    requests.post(url, data=payload)
