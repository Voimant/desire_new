import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
import handlers
import config



async def main():
    TOKEN = config.TOKEN
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    logging.basicConfig(level=logging.INFO)
    dp.include_routers(handlers.router,)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())