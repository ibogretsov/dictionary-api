from typing import Generator

from fastapi import Depends
import pymongo

from app.core import config


def get_db(
        settings: config.Settings = Depends(config.get_settings)
) -> Generator:
    try:
        client = pymongo.MongoClient(settings.dictionary_api_mongodb_url)
        db = client.get_database(settings.db_name)
        yield db
    finally:
        client.close()
