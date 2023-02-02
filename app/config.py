import functools
from typing import Any

import pydantic


class Settings(pydantic.BaseSettings):
    APP_NAME: str = 'Dictionary API'
    DICTIONARY_API_SOURCE_LANGUAGE: str
    DICTIONARY_API_TARGET_LANGUAGE: str

    # Database stuff
    DICTIONARY_API_POSTGRES_HOST: str
    DICTIONARY_API_POSTGRES_PORT: str
    DICTIONARY_API_POSTGRES_USER: str
    DICTIONARY_API_POSTGRES_PASSWORD: str
    DICTIONARY_API_POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: pydantic.PostgresDsn | None

    @pydantic.validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
            cls, v: str | None, values: dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        uri = pydantic.PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("DICTIONARY_API_POSTGRES_USER"),
            password=values.get("DICTIONARY_API_POSTGRES_PASSWORD"),
            host=values.get("DICTIONARY_API_POSTGRES_HOST"),
            port=values.get("DICTIONARY_API_POSTGRES_PORT", 5432),
            path=f"/{values.get('DICTIONARY_API_POSTGRES_DB') or ''}",
        )
        return uri


@functools.lru_cache()
def get_settings() -> Settings:
    return Settings()
