from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Trader Is Training"
    api_prefix: str = "/api"
    database_url: str = Field(
        default="postgresql+psycopg://trader:trader@localhost:5432/trader_is_training"
    )
    cors_origins: list[str] = ["http://localhost:5173"]
    upbit_base_url: str = "https://api.upbit.com"
    upbit_request_interval_seconds: float = 0.12
    upbit_max_retries: int = 3

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")


@lru_cache
def get_settings() -> Settings:
    return Settings()
