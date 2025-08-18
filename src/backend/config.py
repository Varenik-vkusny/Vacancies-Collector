from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    api_base_url: str
    bot_token: str
    rabbitmq_url: str
    redis_url: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

@lru_cache
def get_settings():
    return Settings()


def get_test_settings():
    return Settings(
        database_url="sqlite+aiosqlite:///:memory:",
        redis_url="redis://localhost:6380/1",
        bot_token="fake_bot_token",
        api_base_url="http://test"
    )