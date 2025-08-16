import logging
import asyncio
import aio_pika
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .routers import keywords, users
from src.tg_bot.handlers import common_handlers, register_handler, keywords_handlers
from src.services.tg_send_message import setup_sender
from contextlib import asynccontextmanager
from .config import settings


BOT_TOKEN = settings.bot_token


bot = Bot(BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone = 'Asia/Almaty')


async def put_task_to_queue():
    logging.info('Ложу задачу в очередь')

    try:
        connection = await aio_pika.connect_robust(settings.rabbitmq_url)
        async with connection:
            channel = await connection.channel()

            await channel.default_exchange.publish(
                aio_pika.Message(body=b'start_parsing'),
                routing_key='parsing_queue'
            )
        logging.info('Задача на парсинг отправлена')
    except Exception as e:
        logging.info(f'Не удалось отправить задачу на парсинг: {e}')

@asynccontextmanager
async def lifespan(app: FastAPI):

    logging.info('Приложение запускается')

    loop = asyncio.get_running_loop()

    setup_sender(bot, loop)


    scheduler.add_job(put_task_to_queue, trigger='interval', minutes=30)
    scheduler.start()
    logging.info('Планировщик запущен')

    dp.include_routers(common_handlers.router, register_handler.router, keywords_handlers.router)

    asyncio.create_task(dp.start_polling(bot))

    logging.info('Polling Запущен')

    yield

    logging.info('Приложение останавливается')
    scheduler.shutdown()
    logging.info('Часовщик остановлен')


app = FastAPI(lifespan=lifespan)

app.include_router(keywords.router)
app.include_router(users.router)


@app.get('/')
def read_root():
    return {"message": "Welcome to Vacancies Collector API"}