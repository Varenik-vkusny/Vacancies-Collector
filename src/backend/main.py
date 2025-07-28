import os
import logging
import asyncio
from pathlib import Path
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .routers import jobs, keywords, users
from .database import async_engine, Base
from src.scheduler.jobs_and_users import run_main_parsing
from src.tg_bot.main_bot import router as bot_router
from src.services.tg_send_message import setup_sender
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


current_file_path = Path(__file__).resolve()
print(f"Путь к текущему файлу: {current_file_path}")

project_root = current_file_path.parent.parent.parent

env_path = project_root / ".env"

if env_path.is_file():
    load_dotenv(dotenv_path=env_path, verbose=True)
else:
    print(f"!!! ОШИБКА: .env файл НЕ НАЙДЕН по пути {env_path} !!!")

BOT_TOKEN = os.getenv('BOT_TOKEN')


async def db_init():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()

BOT_TOKEN = os.getenv('BOT_TOKEN')


app.include_router(jobs.router)
app.include_router(keywords.router)
app.include_router(users.router)

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone = 'Asia/Almaty')

@app.on_event('startup')
async def startup():

    logging.info('Приложение запускается')

    loop = asyncio.get_running_loop()

    setup_sender(bot, loop)


    scheduler.add_job(run_main_parsing, trigger='interval', minutes=1)
    scheduler.start()
    logging.info('Планировщик запущен')

    dp.include_router(bot_router)

    asyncio.create_task(dp.start_polling(bot))

    logging.info('Polling Запущен')

    await db_init()

@app.on_event('shutdown')
async def on_shudown():
    logging.info('Приложение останавливается')
    scheduler.shutdown()
    logging.info('Часовщик остановлен')