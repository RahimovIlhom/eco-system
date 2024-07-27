import asyncio
import logging
import sys

from loader import dp, bot, create_db, close_db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup():
    await set_default_commands()
    await on_startup_notify()
    await create_db()


async def on_shutdown():
    await close_db()


async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
