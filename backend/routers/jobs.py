from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.post('/jobs', response_model=schemas.JobsOut, status_code=status.HTTP_201_CREATED)
async def add_job(job: schemas.JobsIn, db: AsyncSession = Depends(get_db)):
    db_job_query = select(models.Jobs).filter(models.Jobs.url == job.url)

    db_job_result = await db.execute(db_job_query)

    db_job = db_job_result.scalar_one_or_none()

    if db_job:
        return
    
    db_job = models.Jobs(**job.dict())

    db.add(db_job)

    await db.commit()

    await db.refresh(db_job)

    users_query = select(models.User)

    users_result = await db.execute(users_query)

    users = users_result.scalars().all()

    for user in users:
        if user.keyword in db_job['title'] or db_job['discription']:
            return db_job
    return