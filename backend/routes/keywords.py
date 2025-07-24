from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import schemas, models
from ..database import get_db

router = APIRouter()


@router.post('/users/keywords', response_model=schemas.KeywordsOut, status_code=status.HTTP_201_CREATED)
async def create_keywords(keywords: schemas.KeywordsIn, telegram_id: int, db: AsyncSession = Depends(get_db)):

    db_keywords_query = select(models.Keyword.text).filter(models.User.telegram_id == telegram_id)
    db_keywords_result = await db.execute(db_keywords_query)
    db_keywords = db_keywords_result.scalar_one_or_none()

    if db_keywords:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='У вас уже есть ключевые слова, если вы хотите написать другие, используйте кнопку изменения ключевых слов.'
        )
    
    db_keywords = models.Keyword(text=keywords.text)

    db.add(db_keywords)
    await db.commit(db_keywords)
    await db.refresh(db_keywords)

    return db_keywords