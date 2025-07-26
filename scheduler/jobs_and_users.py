import logging
from fastapi import Depends
from ..backend.database import get_db
from ..backend import models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from typing import Set, List, Dict, Any


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def get_jobs_hashes(db: AsyncSession = Depends(get_db)) -> Set[str]:

    logging.info('Получение хэшей вакансий.')

    jobs_hashes_query = select(models.User).options(select(models.User.keyword))

    jobs_result = await db.execute(jobs_hashes_query)

    jobs_hashes = set(jobs_result.scalars().all())

    logging.info(f'Получено {len(jobs_hashes)}')

    return jobs_hashes


async def get_active_users_with_keywords(db: AsyncSession = Depends(get_db)):

    logging.info('Беру всех активных пользователей.')

    users_query = select(models.User).options(joinedload(models.User.keyword)).filter(models.User.is_active == True)

    users_result = await db.execute(users_query)

    users = users_result.unique().scalars().all()

    logging.info(f'Получил {len(users)} пользователей')

    return users


async def save_new_jobs(jobs: List[Dict[str, str]], db: AsyncSession = Depends(get_db)):

    logging.info(f'Сохраняю {len(jobs)} новых записей')

    new_jobs = [models.Jobs(**job_data) for job_data in jobs]

    db.add_all(new_jobs)

    await db.commit()

    logging.info('Сохранил в базу новые вакансии')