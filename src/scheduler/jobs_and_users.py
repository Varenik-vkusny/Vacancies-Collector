import logging
import asyncio
from src.backend.database import AsyncLocalSession
from src.backend import models
from src.scripts.parsers import kwork_parser, hh_parser
from src.services.tg_send_message import send_notification
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from typing import Set, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_sync_parse(parse_func):

    return parse_func()


async def get_jobs_hashes(db: AsyncSession) -> Set[str]:

    logging.info('Получение хэшей вакансий.')

    jobs_hashes_query = select(models.Jobs.job_hash)

    jobs_result = await db.execute(jobs_hashes_query)

    jobs_hashes = set(jobs_result.scalars().all())

    logging.info(f'Получено {len(jobs_hashes)}')

    return jobs_hashes


async def get_active_users_with_keywords(db: AsyncSession):

    logging.info('Беру всех активных пользователей.')

    users_query = select(models.User).options(joinedload(models.User.keyword)).filter(models.User.is_active == True)

    users_result = await db.execute(users_query)

    users = users_result.unique().scalars().all()

    logging.info(f'Получил {len(users)} пользователей')

    return users


async def save_new_jobs(jobs: List[Dict[str, Any]], db: AsyncSession):

    logging.info(f'Сохраняю {len(jobs)} новых записей')

    new_jobs = [models.Jobs(**job_data) for job_data in jobs]

    db.add_all(new_jobs)

    await db.commit()

    logging.info('Сохранил в базу новые вакансии')


async def run_main_parsing():

    logging.info('Запускаю пасреры и рассылку уведомлений')

    async with AsyncLocalSession() as db:

        try:
            loop = asyncio.get_running_loop()

            with ThreadPoolExecutor() as pool:

                tasks = [
                    get_jobs_hashes(db),
                    get_active_users_with_keywords(db),
                    loop.run_in_executor(pool, run_sync_parse, kwork_parser.parse),
                    loop.run_in_executor(pool, run_sync_parse, hh_parser.parse)
                ]

                results = await asyncio.gather(*tasks, return_exceptions=True)

            existing_hashes = results[0] if not isinstance(results[0], Exception) else set()
            active_users = results[1] if not isinstance(results[1], Exception) else []
            kwork_data = results[2] if not isinstance(results[2], Exception) else []
            hh_data = results[3] if not isinstance(results[3], Exception) else []

            for i, res in enumerate(results):
                if isinstance(res, Exception):
                    logging.info(f'Ошибка в {i} элементе: {res}')

            logging.info('Получил все нужны данные')
                    
            all_parse_data = kwork_data + hh_data
            new_jobs = []
            for job in all_parse_data:
                if job.get('job_hash') and job['job_hash'] not in existing_hashes:
                    new_jobs.append(job)
                    existing_hashes.add(job['job_hash'])
            

            if not new_jobs:
                logging.info('Нет новых вакансий.')
                return
            
            logging.info('Нашел новые вакансии')
            
            await save_new_jobs(new_jobs, db)
            
            notification_tasks = []
            for job in new_jobs:
                job_to_search = f'{job['title']} {job.get('description', '')}'.lower()
                for user in active_users:
                    for keyword in user.keyword:
                        if keyword.text.lower() in job_to_search:
                            task = send_notification(user.telegram_id, job)
                            notification_tasks.append(task)
                            break

            if notification_tasks:
                logging.info(f'Запускаю отправку {len(notification_tasks)} уведомлений...')
                

                notification_results = await asyncio.gather(*notification_tasks, return_exceptions=True)
                
                
                successful_sends = 0
                for i, result in enumerate(notification_results):
                    if isinstance(result, Exception):
                        # Если результат - это исключение, логируем его
                        logging.error(f"Ошибка при отправке уведомления №{i+1}: {result}")
                    else:
                        successful_sends += 1
                
                logging.info(f'Обработка уведомлений завершена. Успешно отправлено: {successful_sends} из {len(notification_tasks)}.')
            logging.info('Парсинг и отправка уведомлений завершена!')
        except Exception as e:
            logging.info(f'Произошла критическая ошибка: {e}', exc_info=True)

    