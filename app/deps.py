from typing import Generator

from fastapi import Depends
from pymongo import MongoClient
from pymongo.database import Database

from app import config


def get_db(
        settings: config.Settings = Depends(config.get_settings)
) -> Generator:
    try:
        client: MongoClient = MongoClient(settings.dictionary_api_mongodb_url)
        db: Database = client.get_database(settings.db_name)
        yield db
    finally:
        client.close()
