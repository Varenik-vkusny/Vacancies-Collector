from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
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


async def _get_user_with_kw_from_db_or_cache(
    telegram_id: int, 
    db: AsyncSession, 
    redis_client: redis.Redis
) -> models.User|None:
    
    cache_key = str(telegram_id)
    cached_user = await redis_client.get(cache_key)

    if cached_user:
        print("CACHE HIT")
        pydantic_user = schemas.UserWithKeywords.model_validate_json(cached_user)
        query = (select(models.User).options(selectinload(models.User.keywords)).filter(models.User.id == pydantic_user.id))
        result = await db.execute(query)
        user_from_db = result.scalar_one_or_none()
        return user_from_db

    print("CACHE MISS")
    user_query = select(models.User).options(selectinload(models.User.keywords)).filter(models.User.telegram_id == telegram_id)
    user_from_db = (await db.execute(user_query)).unique().scalar_one_or_none()

    if not user_from_db:
        return None 

    
    pydantic_user = schemas.UserWithKeywords.model_validate(user_from_db)
    await redis_client.set(cache_key, pydantic_user.model_dump_json(), ex=600)
    
    return user_from_db


async def get_user_with_keywords_by_tg_id(
    telegram_id: int, 
    redis_client: redis.Redis = Depends(get_redis_client), 
    db: AsyncSession = Depends(get_db)
) -> models.User:
    
    user = await _get_user_with_kw_from_db_or_cache(telegram_id, db, redis_client)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return user