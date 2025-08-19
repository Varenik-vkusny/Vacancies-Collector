import pytest
from unittest.mock import AsyncMock, MagicMock
from src.backend import schemas, models
from src.backend.dependencies import get_user_with_kw_from_db_or_cache

@pytest.mark.anyio
async def test_redis_cache_hit():

    test_redis = AsyncMock()
    test_db = AsyncMock()

    fake_data = schemas.UserWithKeywords(
        id=15,
        telegram_id=123,
        name='Тимурка',
        keywords=[]
    )

    test_redis.get.return_value = fake_data.model_dump_json()

    result = await get_user_with_kw_from_db_or_cache(fake_data.telegram_id, test_db, test_redis)

    test_redis.get.assert_awaited_once_with(str(fake_data.telegram_id))
    test_db.execute.assert_not_called()

    assert result.id == fake_data.id


@pytest.mark.anyio
async def test_redis_cache_miss():

    test_redis = AsyncMock()
    test_db = AsyncMock()

    fake_data = models.User(
        id=25,
        telegram_id=456,
        name='Тимур',
        keywords=[]
    )

    test_redis.get.return_value = None


    mock_result = MagicMock()
    mock_result.unique.return_value.scalar_one_or_none.return_value = fake_data

    test_db.execute.return_value = mock_result

    result = await get_user_with_kw_from_db_or_cache(fake_data.telegram_id, test_db, test_redis)

    test_redis.get.assert_awaited_once_with(str(fake_data.telegram_id))
    test_db.execute.assert_awaited_once()

    assert result.id == fake_data.id