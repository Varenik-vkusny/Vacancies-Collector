import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path

current_file_path = Path(__file__)

project_root = current_file_path.parent.parent.parent

env_path = project_root / '.env'

load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv('DATABASE_URL')

async_engine = create_async_engine(DATABASE_URL, echo=True)

AsyncLocalSession = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with AsyncLocalSession() as session:
        yield session