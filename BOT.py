import asyncio
from aiogram import Bot, Dispatcher
from handlers import handlers
from config.config import load_config
import logging

async def main():
    config = load_config()

    bot = Bot(token=config.tg_bot.token)

    dp = Dispatcher()
    dp.include_router(handlers.router)

    await dp.start_polling(bot), 




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())