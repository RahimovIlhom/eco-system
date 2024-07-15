from aiogram import types

from loader import bot


async def set_default_commands():
    commands = [
            types.BotCommand(command="start", description="Botni ishga tushurish"),
            types.BotCommand(command="help", description="Yordam"),
        ]
    await bot.set_my_commands(
        commands, types.BotCommandScopeDefault()
    )
