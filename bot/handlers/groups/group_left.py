from aiogram import types
from aiogram.exceptions import TelegramBadRequest

from loader import dp, bot
from filters import ChatTypeFilter
from data.config import ADMINS


@dp.message(ChatTypeFilter(['group', 'supergroup']), lambda msg: msg.content_type == types.ContentType.LEFT_CHAT_MEMBER)
async def left_chat_member_handler(message: types.Message):
    if message.left_chat_member.is_bot:
        bot_mention = message.left_chat_member.mention_html(message.left_chat_member.full_name)
        group_title = message.chat.title
        kicked_member_mention = message.from_user.mention_html(message.from_user.first_name)
        # Bot guruhdan chiqarilganda amalga oshiriladigan harakatlar
        for admin in ADMINS:
            await message.bot.send_message(admin, f"{bot_mention} boti {group_title} guruhdan {kicked_member_mention} tomonidan chiqarildi!")
