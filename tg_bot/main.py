import asyncio

from aiogram import Bot, Dispatcher

from tg_bot.handlers.user_private import user_private_router

bot = Bot(token='7523548334:AAGre6B5Nf7MnIuw78vDBgbUBovCVuSbSfs')

dp = Dispatcher()

dp.include_router(user_private_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

