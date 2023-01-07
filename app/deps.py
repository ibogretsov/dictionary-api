from typing import Generator

import pymongo

from app.settings.config import settings


def get_db() -> Generator:
    try:
        client = pymongo.MongoClient(settings.dictionary_api_mongodb_url)
        db = client.get_database(settings.db_name)
        yield db
    finally:
        client.close()
