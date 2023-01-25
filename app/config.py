import functools
from typing import Any

import pydantic


class Settings(pydantic.BaseSettings):
    app_name: str = 'Dictionary API'

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

    dictionary_api_source_language: str
    dictionary_api_target_language: str


@functools.lru_cache()
def get_settings() -> Settings:
    return Settings()
