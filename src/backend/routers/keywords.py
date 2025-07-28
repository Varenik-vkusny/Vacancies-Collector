from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.backend import schemas, models
from src.backend.database import get_db

router = APIRouter()


@router.post('/keywords', response_model=schemas.KeywordsOut, status_code=status.HTTP_201_CREATED)
async def create_keywords(keyword: schemas.KeywordsIn, db: AsyncSession = Depends(get_db)):

    user_query = select(models.User).filter(models.User.telegram_id == keyword.telegram_id)

    user_result = await db.execute(user_query)

    user = user_result.scalar_one_or_none()    

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )

    db_keywords_exists = select(models.Keywords).filter(models.Keywords.user_id == user.id)

    db_keywords_result = await db.execute(db_keywords_exists)

    db_keywords = db_keywords_result.scalar_one_or_none()

    if db_keywords:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='У вас уже есть ключевые слова, если вы хотите написать другие, используйте кнопку изменения ключевых слов.'
        )
    
    db_keywords = models.Keywords(text=keyword.text, user_id = user.id)

    db.add(db_keywords)
    await db.commit()
    await db.refresh(db_keywords)

    return db_keywords


@router.get('/keywords/{telegram_id}', response_model=schemas.KeywordsOut, status_code=status.HTTP_200_OK)
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

    db_keyword = db_keyword_result.scalar_one_or_none()

    if not db_keyword:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='У вас нет заданных ключевых слов.'
        )
    
    return db_keyword


@router.put('/keywords', response_model=schemas.KeywordsOut, status_code=status.HTTP_200_OK)
async def put_keyword(new_keyword: schemas.KeywordsIn, db: AsyncSession = Depends(get_db)):

    user_query = select(models.User).filter(models.User.telegram_id == new_keyword.telegram_id)

    user_result = await db.execute(user_query)

    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )

    db_keyword_query = select(models.Keywords).filter(models.Keywords.user_id == user.id)

    db_keyword_result = await db.execute(db_keyword_query)

    db_keyword = db_keyword_result.scalar_one_or_none()

    if not db_keyword:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='У вас нет заданных ключевых слов, задайте новые.'
        )
    
    db_keyword = models.Keywords(**new_keyword.dict(), user_id=user.id)

    db.add(db_keyword)

    await db.commit()

    return db_keyword


@router.delete('/keywords/{telegram_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_keyword(telegram_id: int, db: AsyncSession = Depends(get_db)):

    user_query = select(models.User).filter(models.User.telegram_id == telegram_id)

    user_result = await db.execute(user_query)

    user = user_result.scalar_one_or_none()

    db_keyword_query = select(models.Keywords).filter(models.Keywords.user_id == user.id)

    db_keyword_result = await db.execute(db_keyword_query)

    db_keyword = db_keyword_result.scalar_one_or_none()

    if not db_keyword:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='У вас нет заданных ключевых слов, чтобы удалить ключи сначала задайте новые.'
        )
    
    await db.delete(db_keyword)

    await db.commit()