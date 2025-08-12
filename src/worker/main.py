import aio_pika
import logging
import asyncio
from src.scheduler.jobs_and_users import run_main_parsing
from src.backend.config import settings

logging.basicConfig(level=logging.INFO)

async def main():
    logging.info('Запускаю воркера')

    logging.info('Создаю соединение')
    connection = await aio_pika.connect_robust(settings.rabbitmq_url)

    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue('parsing_queue', durable=True)

        logging.info('Воркер готов к работе, ожидание задач...')

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    if message.body == b'start_parsing':
                        logging.info('Запускаю задачу')
                        try:
                            await run_main_parsing()
                            logging.info('Парсинг запущен')
                        except Exception as e:
                            logging.info(f'Парсинг упал с ошибкой: {e}')

                    if queue.name == message.body.decode():
                        break


if __name__ == '__main__':
    asyncio.run(main())