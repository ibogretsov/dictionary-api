from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.results import DeleteResult
from pymongo.results import InsertOneResult


class WordDBManager:

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._db = db
        self._collection = self._db.words

    async def insert_word_info(
            self,
            word_details: dict[str, Any]
    ) -> InsertOneResult:
        result: InsertOneResult = await self._collection.insert_one(
            word_details
        )
        return result

    async def get_word(self, word: str) -> Any:
        result = await self._collection.find_one({'word': word})
        return result

    async def delete_word(self, word: str) -> DeleteResult:
        result: DeleteResult = await self._collection.delete_one({'word': word})
        return result
