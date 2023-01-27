import functools
from typing import Any

import pydantic


class Settings(pydantic.BaseSettings):
    APP_NAME: str = 'Dictionary API'
    DICTIONARY_API_SOURCE_LANGUAGE: str
    DICTIONARY_API_TARGET_LANGUAGE: str

    # Database stuff
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: pydantic.PostgresDsn | None

    @pydantic.validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
            cls, v: str | None, values: dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return pydantic.PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


@functools.lru_cache()
def get_settings() -> Settings:
    return Settings()
