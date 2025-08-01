from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend import schemas, models
from src.backend.database import get_db
from sqlalchemy import select


router = APIRouter()

@router.post('/users/register', response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def user_register(user: schemas.UserIn, db: AsyncSession = Depends(get_db)):

    db_user_query = select(models.User).filter(models.User.telegram_id == user.telegram_id)

    db_user_result = await db.execute(db_user_query)

    db_user = db_user_result.scalar_one_or_none()

    if db_user:
        db_user.name = user.name

        db_user.is_active = True
    else:
        db_user = models.User(**user.model_dump())

        db.add(db_user)

    await db.commit()

    await db.refresh(db_user)

    return db_user


