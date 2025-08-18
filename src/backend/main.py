import logging
import aio_pika
import redis.asyncio as redis
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .routers import keywords, users
from contextlib import asynccontextmanager
from .config import get_settings
from . import clients

settings = get_settings()


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

    clients.redis_client = redis.from_url(settings.redis_url, encoding='utf-8', decode_responses=True)
    logging.info('Redis подключен')

    scheduler.add_job(put_task_to_queue, trigger='interval', minutes=30)
    scheduler.start()
    logging.info('Планировщик запущен')

    yield

    logging.info('Приложение останавливается')
    scheduler.shutdown()
    logging.info('Часовщик остановлен')

    if clients.redis_client:
        await clients.redis_client.close()
        logging.info('Redis остановлен')


app = FastAPI(lifespan=lifespan)

app.include_router(keywords.router)
app.include_router(users.router)


@app.get('/')
def read_root():
    return {"message": "Welcome to Vacancies Collector API"}