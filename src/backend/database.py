from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

DATABASE_URL = settings.database_url

async_engine = create_async_engine(DATABASE_URL, echo=True)

AsyncLocalSession = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()
from . import models