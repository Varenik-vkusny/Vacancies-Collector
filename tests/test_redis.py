import pytest
from unittest.mock import AsyncMock
from src.backend import schemas
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