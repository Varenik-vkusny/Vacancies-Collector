from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import redis.asyncio as redis
from .database import AsyncLocalSession
from . import models, schemas
from .clients import get_redis_client


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


async def get_user_with_kw_from_db_or_cache(telegram_id: int, db: AsyncSession = Depends(get_db), redis_client: redis.Redis = Depends(get_redis_client)) -> schemas.UserWithKeywords:
    
    cache_key = str(telegram_id)
    cached_user = await redis_client.get(cache_key)

    if cached_user:
        print("CACHE HIT")

        return schemas.UserWithKeywords.model_validate_json(cached_user)

    print("CACHE MISS")
    user_query = select(models.User).options(selectinload(models.User.keywords)).filter(models.User.telegram_id == telegram_id)
    user_from_db = (await db.execute(user_query)).unique().scalar_one_or_none()

    if not user_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        ) 

    
    pydantic_user = schemas.UserWithKeywords.model_validate(user_from_db)
    await redis_client.set(cache_key, pydantic_user.model_dump_json(), ex=600)
    
    return pydantic_user


async def get_user_with_keywords_by_tg_id(
    telegram_id: int, 
    db: AsyncSession = Depends(get_db)
) -> models.User:
    
    user_query = select(models.User).options(selectinload(models.User.keywords)).filter(models.User.telegram_id == telegram_id)
    user_from_db = (await db.execute(user_query)).unique().scalar_one_or_none()

    if not user_from_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    
    return user_from_db