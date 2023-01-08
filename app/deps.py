import functools
from typing import Generator

from fastapi import Depends
import pymongo

from app.settings.config import Settings


@functools.lru_cache()
def get_settings() -> Settings:
    return Settings()


def get_db(settings: Settings = Depends(get_settings)) -> Generator:
    try:
        client = pymongo.MongoClient(settings.dictionary_api_mongodb_url)
        db = client.get_database(settings.db_name)
        yield db
    finally:
        client.close()
