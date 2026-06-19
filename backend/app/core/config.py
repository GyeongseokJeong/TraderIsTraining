import json
from functools import lru_cache
from typing import Annotated, Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Trader Is Training"
    api_prefix: str = "/api"
    database_url: str = Field(
        default="postgresql+psycopg://trader:trader@localhost:5432/trader_is_training"
    )
    cors_origins: Annotated[list[str], NoDecode] = ["http://localhost:5173"]
    upbit_base_url: str = "https://api.upbit.com"
    upbit_request_interval_seconds: float = 0.12
    upbit_max_retries: int = 3

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> Any:
        if isinstance(value, list):
            return value

        if isinstance(value, str):
            stripped_value = value.strip()
            if stripped_value.startswith("["):
                try:
                    parsed_value = json.loads(stripped_value)
                except json.JSONDecodeError as exc:
                    parsed_value = cls._parse_unquoted_origin_list(stripped_value)
                    if parsed_value is None:
                        raise ValueError(
                            "CORS_ORIGINS must be a JSON array string or a comma-separated string."
                        ) from exc

                if not isinstance(parsed_value, list):
                    raise ValueError(
                        "CORS_ORIGINS JSON value must be an array of origin strings."
                    )
                return parsed_value

            return [
                origin.strip() for origin in stripped_value.split(",") if origin.strip()
            ]

        return value

    @staticmethod
    def _parse_unquoted_origin_list(value: str) -> list[str] | None:
        if not value.endswith("]"):
            return None

        inner_value = value[1:-1]
        origins = [
            origin.strip() for origin in inner_value.split(",") if origin.strip()
        ]
        if not origins:
            return None

        return origins

    model_config = SettingsConfigDict(
        env_file=".env", env_nested_delimiter="__", extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
