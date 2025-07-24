from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import schemas, models
from ..database import get_db

router = APIRouter()


@router.post('/keywords', response_model=schemas.KeywordsOut, status_code=status.HTTP_201_CREATED)
async def create_keywords(keywords: schemas.KeywordsIn, db: AsyncSession = Depends(get_db)):

    db_keywords_exists = select(models.Keywords).filter(models.Keywords.text == keywords.text)

    db_keywords_result = await db.execute(db_keywords_exists)

    db_keywords = db_keywords_result.scalar_one_or_none()

    if db_keywords:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='У вас уже есть ключевые слова, если вы хотите написать другие, используйте кнопку изменения ключевых слов.'
        )
    
    db_keywords = models.Keywords(text=keywords.text)

    db.add(db_keywords)
    await db.commit()
    await db.refresh(db_keywords)

    return db_keywords


@router.get('/keywords/{user_id}', response_model=schemas.KeywordsOut, status_code=status.HTTP_200_OK)
async def get_keywords(user_id: int, db: AsyncSession = Depends(get_db)):
    db_keyword_query = select(models.Keywords).filter(models.Keywords.user_id == user_id)

    db_keyword_result = await db.execute(db_keyword_query)

    db_keyword = db_keyword_result.scalar_one_or_none()

    if not db_keyword:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='У вас нет заданных ключевых слов.'
        )
    
    return db_keyword