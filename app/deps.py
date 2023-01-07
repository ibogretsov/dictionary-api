from typing import Generator

import motor.motor_asyncio

from app.settings.config import settings


def get_db() -> Generator:
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(
            settings.dictionary_api_mongodb_url
        )
        db = client.get_database('dictionarydb')
        yield db
    finally:
        client.close()
