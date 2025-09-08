from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
from functools import lru_cache


class Settings(BaseSettings):

    db_host: str
    db_port: int
    db_driver: str
    db_user: str
    db_password: str
    db_name: str

    api_base_url: str
    bot_token: str

    rabbitmq_host: str
    rabbitmq_user: str
    rabbitmq_password: str
    rabbitmq_port: int

    redis_host: str
    redis_port: int
    redis_db: int

    @computed_field
    @property
    def database_url(self) -> str:
        return f"{self.db_driver}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @computed_field
    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    @computed_field
    @property
    def rabbitmq_url(self) -> str:
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}/"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings():
    return Settings()


def get_test_settings():
    return Settings(
        redis_host="localhost",
        redis_port=6380,
        redis_db=1,
        bot_token="fake_bot_token",
        api_base_url="http://test",
    )
