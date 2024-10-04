import asyncio
from datetime import timedelta

import uvicorn
from aiogram import Bot, Dispatcher
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from backend.auth.backend import auth_backend
from backend.auth.schemas import UserRead, UserCreate
from backend.botSettings.crud import get_last_active_raffle, get_current_raffle
from backend.botSettings.routers import fastapi_users, router_admin, router_all_user
from tg_bot.cron.generate_winners import monitor_raffles
#from tg_bot.cron.generate_winners import determine_and_notify_winners, monitor_raffles
from tg_bot.db.engine import async_session_maker
from tg_bot.handlers.user_private import user_private_router
from tg_bot.middlewares.db import DataBaseSession
from tg_bot.middlewares.time_check import TimeCheckMiddleware

scheduler = AsyncIOScheduler()

bot = Bot(token='7523548334:AAGre6B5Nf7MnIuw78vDBgbUBovCVuSbSfs')
dp = Dispatcher()

dp.include_router(user_private_router)

app = FastAPI()

app.include_router(router_admin,
                   prefix='/admin',
                   tags=['modification'])
app.include_router(router_all_user,
                   prefix='/manager',
                   tags=['browse'])
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],)

async def monitor_raffle():
    async with async_session_maker() as session:
        monitor_task = asyncio.create_task(monitor_raffles(bot, session))
        await monitor_task


async def start_bot():
    dp.update.middleware(DataBaseSession(session_pool=async_session_maker))
    dp.update.middleware(TimeCheckMiddleware(session_maker=async_session_maker))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def start_api():
    config = uvicorn.Config(app, host="localhost", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await asyncio.gather(start_bot(), start_api(), monitor_raffle())

if __name__ == "__main__":
    asyncio.run(main())
