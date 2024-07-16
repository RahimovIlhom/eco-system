from aiogram import types
from aiogram.exceptions import TelegramBadRequest

from loader import dp, bot
from filters import ChatTypeFilter
from data.config import ADMINS


@dp.message(ChatTypeFilter(['group', 'supergroup']), lambda msg: msg.content_type == types.ContentType.NEW_CHAT_MEMBERS)
async def join_chat_member_handler(message: types.Message):
    for member in message.new_chat_members:
        if member.is_bot:
            await senf_msg_to_admins(message, member)


async def senf_msg_to_admins(message: types.Message, member):
    bot_title = member.mention_html(member.full_name)
    try:
        group_invite_link = await bot.export_chat_invite_link(chat_id=message.chat.id)
        group_mention = f'<a href="{group_invite_link}">{message.chat.title}</a>'
    except TelegramBadRequest:
        group_mention = f"<b>{message.chat.title}</b>"
    added_member_mention = message.from_user.mention_html(message.from_user.first_name)

    for admin in ADMINS:
        await message.bot.send_message(admin, f"{bot_title} boti {group_mention} guruhga {added_member_mention} tomonidan qo'shildi!")
    return
