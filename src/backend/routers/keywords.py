from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from src.backend import schemas, models
from src.backend.database import get_db

router = APIRouter()


@router.post('/keywords', response_model=schemas.KeywordsOut, status_code=status.HTTP_201_CREATED)
async def create_keywords(keyword: schemas.KeywordsIn, db: AsyncSession = Depends(get_db)):

    user_query = select(models.User).options(joinedload(models.User.keywords)).filter(models.User.telegram_id == keyword.telegram_id)

    user_result = await db.execute(user_query)

    user = user_result.unique().scalar_one_or_none()    

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )
    
    for user_keyword in user.keywords:

        db_keyword_exists = select(models.User).filter(user_keyword == keyword.text)

        db_keyword_result = await db.execute(db_keyword_exists)

        db_keyword = db_keyword_result.scalar_one_or_none()

        if db_keyword:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='У вас уже есть такое ключевое слово'
            )
    
    db_keywords = models.Keywords(text=keyword.text, user_id = user.id)

    db.add(db_keywords)
    await db.commit()
    await db.refresh(db_keywords)

    return db_keywords


@router.get('/keywords', response_model=list[schemas.KeywordsOut], status_code=status.HTTP_200_OK)
async def get_keywords(telegram_id: int, db: AsyncSession = Depends(get_db)):

    user_query = select(models.User).filter(models.User.telegram_id == telegram_id)

    user_result = await db.execute(user_query)

    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )
    

    db_keyword_query = select(models.Keywords).filter(models.Keywords.user_id == user.id)

    db_keyword_result = await db.execute(db_keyword_query)

    db_keywords = db_keyword_result.scalars().all()

    if not db_keywords:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='У вас нет заданных ключевых слов.'
        )
    
    return db_keywords


@router.delete('/keywords', status_code=status.HTTP_204_NO_CONTENT)
async def delete_keyword(telegram_id: int, keyword_text: str, db: AsyncSession = Depends(get_db)):

    user_with_keywords_query = select(models.User).options(joinedload(models.User.keywords)).filter(models.User.telegram_id == telegram_id)

    user_result = await db.execute(user_with_keywords_query)

    user = user_result.unique().scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )
    
    if not user.keywords:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='У вас нет заданных ключевых слов, чтобы удалить ключи сначала задайте новые'
        )
    
    for keyword in user.keywords:

        if keyword.text == keyword_text:
            await db.delete(keyword)

            await db.commit()

            return
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='У вас нет такого ключевого слова'
    )