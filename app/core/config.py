import functools

import pydantic


class Settings(pydantic.BaseSettings):
    app_name: str = 'Dictionary API'
    dictionary_api_mongodb_url: str | None
    db_name: str = 'dictionarydb'
    dictionary_api_source_language: str
    dictionary_api_target_language: str


@functools.lru_cache()
def get_settings() -> Settings:
    return Settings()
