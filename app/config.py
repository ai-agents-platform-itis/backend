from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    driver: str
    host: str
    user: str
    password: str
    port: int
    name: str


class RedisSettings(BaseSettings):
    host: str
    port: int
    db: int


class OpenAISettings(BaseSettings):
    api_key: str


class AppSettings(BaseSettings):
    secret_key: str
    debug: bool
    name: str


class Settings(BaseSettings):
    db: DatabaseSettings
    redis: RedisSettings
    openai: OpenAISettings
    app: AppSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_nested_delimiter="__",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()