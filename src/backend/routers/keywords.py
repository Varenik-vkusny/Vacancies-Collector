from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis
from .. import schemas, models
from ..dependencies import get_db
from ..dependencies import get_user_with_keywords_by_tg_id, _get_user_with_kw_from_db_or_cache
from ..clients import get_redis_client

router = APIRouter()


@router.post('/keywords', response_model=schemas.KeywordsOut, status_code=status.HTTP_201_CREATED)
async def create_keywords(keyword: schemas.KeywordsIn, redis_client: redis.Redis = Depends(get_redis_client), db: AsyncSession = Depends(get_db)):

    user = await _get_user_with_kw_from_db_or_cache(telegram_id=keyword.telegram_id, db=db, redis_client=redis_client)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )
    
    for user_keyword in user.keywords:
        if user_keyword.text == keyword.text:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='У вас уже есть такое ключевое слово'
            )
    
    db_keywords = models.Keywords(text=keyword.text, user_id = user.id)

    db.add(db_keywords)
    await db.commit()
    await db.refresh(db_keywords)
    await redis_client.delete(str(keyword.telegram_id))

    return db_keywords


@router.get('/keywords', response_model=list[schemas.KeywordsOut], status_code=status.HTTP_200_OK)
async def get_keywords(user: models.User = Depends(get_user_with_keywords_by_tg_id)):

    if not user.keywords:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='У вас нет заданных ключевых слов.'
        )
    
    keywords = user.keywords
    
    return keywords


@router.delete('/keywords', status_code=status.HTTP_204_NO_CONTENT)
async def delete_keyword(keyword_text: str, redis_client: redis.Redis = Depends(get_redis_client), user: models.User = Depends(get_user_with_keywords_by_tg_id), db: AsyncSession = Depends(get_db)):

    if not user.keywords:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='У вас нет заданных ключевых слов, чтобы удалить ключи сначала задайте новые'
        )
    
    for keyword in user.keywords:

        if keyword.text == keyword_text:
            await db.delete(keyword)

            await db.commit()

            await redis_client.delete(str(user.telegram_id))

            return 
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='У вас нет такого ключевого слова'
    )