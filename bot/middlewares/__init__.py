import asyncio

from aiogram import Router

from middlewares.throttling import ThrottlingMiddleware

loop = asyncio.get_event_loop()
redis_url = "redis://localhost"  # Redis URL
router = Router()
router.message.middleware(ThrottlingMiddleware(redis_url))
