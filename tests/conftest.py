import pytest
import redis.asyncio as redis
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from src.backend.main import app
from src.backend.database import Base
from src.backend.dependencies import get_db
from src.backend.config import get_settings, get_test_settings
from src.backend.clients import get_redis_client

app.dependency_overrides[get_settings] = get_test_settings

TEST_DATABASE_URL = 'sqlite+aiosqlite:///:memory:'


test_async_engine = create_async_engine(TEST_DATABASE_URL)


TestAsyncSessionLocal = sessionmaker(bind=test_async_engine, class_=AsyncSession, expire_on_commit=False)


async def override_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestAsyncSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_db


async def override_redis_client():

    test_settings = get_test_settings()
    return redis.from_url(test_settings.redis_url, encoding='utf-8', decode_responses=True)


app.dependency_overrides[get_redis_client] = override_redis_client

@pytest.fixture(autouse=True, scope='function')
async def prepare_database():
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
async def client() -> AsyncGenerator[AsyncClient, None]:

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='function')
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestAsyncSessionLocal() as session:
        yield session