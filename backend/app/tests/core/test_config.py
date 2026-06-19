import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_cors_origins_keeps_list_values() -> None:
    origins = ["http://localhost:15173"]

    settings = Settings(cors_origins=origins)

    assert settings.cors_origins == origins


def test_cors_origins_parses_json_array_string() -> None:
    settings = Settings(cors_origins='["http://localhost:15173"]')

    assert settings.cors_origins == ["http://localhost:15173"]


def test_cors_origins_parses_comma_separated_string() -> None:
    settings = Settings(
        cors_origins="http://localhost:15173, http://127.0.0.1:15173"
    )

    assert settings.cors_origins == [
        "http://localhost:15173",
        "http://127.0.0.1:15173",
    ]


def test_cors_origins_parses_comma_separated_env_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "CORS_ORIGINS", "http://localhost:15173,http://127.0.0.1:15173"
    )

    settings = Settings()

    assert settings.cors_origins == [
        "http://localhost:15173",
        "http://127.0.0.1:15173",
    ]


def test_cors_origins_rejects_invalid_json_array_string() -> None:
    with pytest.raises(ValidationError, match="JSON array string or a comma-separated string"):
        Settings(cors_origins='["http://localhost:15173"')
