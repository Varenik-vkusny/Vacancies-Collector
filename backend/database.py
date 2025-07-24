from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'here database'

async_engine = create_async_engine(DATABASE_URL, echo=True)

AsyncLocalSession = sessionmaker(bond=async_engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    with AsyncLocalSession as session:
        yield session