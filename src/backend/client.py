import redis.asyncio as redis
from .config import get_settings, Settings
from fastapi import Depends

settings = get_settings()

def get_redis_client(settings: Settings = Depends(get_settings)):
    return redis.from_url(settings.redis_url, encoding='utf-8', decode_responses=True)