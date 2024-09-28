from datetime import datetime
from aiogram import BaseMiddleware
from aiogram.types import Update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from backend.botSettings.crud import get_lifetime_dates


class TimeCheckMiddleware(BaseMiddleware):
    def __init__(self, session_maker: async_sessionmaker):
        self.session_maker = session_maker

    async def __call__(self, handler, event: Update, data):
        async with self.session_maker() as session:
            current_time = datetime.now()
            lifetime_bot = await get_lifetime_dates(session=session)

            if lifetime_bot.time_end > current_time > lifetime_bot.time_start:
                return await handler(event, data)
            else:
                message = event.message
                if message:
                    await message.answer('Розыгрышей в данный момент нет')
                return
