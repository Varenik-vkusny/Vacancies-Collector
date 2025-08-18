import logging
import asyncio
from aiogram import Bot, Dispatcher
from src.backend.config import get_settings
from .handlers import common_handlers, keywords_handlers, register_handler
from src.services.tg_send_message import setup_sender

settings = get_settings()

logging.basicConfig(level=logging.INFO)

async def main():

    logging.info('Запускаю бота')

    bot = Bot(settings.bot_token)
    dp = Dispatcher()

    loop = asyncio.get_running_loop()

    setup_sender(bot, loop)

    dp.include_router(common_handlers.router)
    dp.include_router(keywords_handlers.router)
    dp.include_router(register_handler.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())