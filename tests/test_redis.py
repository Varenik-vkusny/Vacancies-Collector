# import pytest
# import redis.asyncio as redis
# from fastapi import Depends
# from unittest.mock import AsyncMock
# from src.backend.clients import get_redis_client
# from src.backend import schemas

# @pytest.mark.anyio
# async def test_redis_cache_hit(redis_client: redis.Redis = Depends(get_redis_client)):

#     test_redis = AsyncMock
#     test_db = AsyncMock

#     fake_data = schemas.UserWithKeywords(
#         id=15,
#         telegram_id=123,
#         name='Тимурка',
#         keywords=[]
#     )

#     test_redis.get.return_value = fake_data.