from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, models
from ..database import get_db
from sqlalchemy import select


router = APIRouter()

@router.post('/users/register', response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def user_register(user: schemas.UserIn, db: AsyncSession = Depends(get_db)):

    db_user_query = select(models.User).filter(models.User.telegram_id == user.telegram_id)

    db_user_result = await db.execute(db_user_query)

    db_user = db_user_result.scalar_one_or_none()

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с таким id уже есть'
        )
    
    db_user = models.User(**user.dict())

    db.add(db_user)

    await db.commit()

    await db.refresh(db_user)

    return db_user


