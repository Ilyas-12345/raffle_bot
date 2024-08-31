import asyncio

import uvicorn
from aiogram import Bot, Dispatcher
from fastapi import FastAPI

from backend.botSettings.routers import router
from tg_bot.db.engine import async_session_maker
from tg_bot.handlers.user_private import user_private_router
from tg_bot.middlewares.db import DataBaseSession

bot = Bot(token='7523548334:AAGre6B5Nf7MnIuw78vDBgbUBovCVuSbSfs')

dp = Dispatcher()

dp.include_router(user_private_router)

app = FastAPI()

app.include_router(router=router)

async def main():
    dp.update.middleware(DataBaseSession(session_pool=async_session_maker))
    await bot.delete_webhook(drop_pending_updates=True)
    uvicorn.run(app, host="localhost",port=8080, log_level="info")


if __name__ == "__main__":
    asyncio.run(main())

