from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from .database import AsyncLocalSession
from . import models, schemas


async def get_db():
    async with AsyncLocalSession() as session:
        yield session



async def get_user_by_tg_id(telegram_id: int, db: AsyncSession = Depends(get_db)) -> models.User:

    user_query = select(models.User).filter(models.User.telegram_id == telegram_id)

    user_result = await db.execute(user_query)

    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )
    
    return user


async def get_user_with_keywords_by_tg_id(telegram_id: int, db: AsyncSession = Depends(get_db)) -> models.User:

    user_query = select(models.User).options(joinedload(models.User.keywords)).filter(models.User.telegram_id == telegram_id)

    user_result = await db.execute(user_query)

    user = user_result.unique().scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )
    
    return user