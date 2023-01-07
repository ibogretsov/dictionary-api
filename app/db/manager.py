from typing import Any, Mapping

from motor.motor_asyncio import AsyncIOMotorDatabase
import pymongo
from pymongo.results import DeleteResult
from pymongo.results import InsertOneResult

from app import constants


class WordDBManager:

    __sort_map = {
        constants.SortTypeEnum.asc.value: pymongo.ASCENDING,
        constants.SortTypeEnum.desc.value: pymongo.DESCENDING
    }

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

    async def get_words(
        self,
        sort: str,
        search_pattern: str | None = None,
        **columns: Mapping[str, bool],
    ):
        search_params: dict[str, dict[str, str]] = {}
        if search_pattern:
            search_params = {
                'word': {
                    '$regex': search_pattern,
                    '$options': 'i'
                }
            }
        exclude_columns_list: list[str] = ['_id']
        for column, val in columns.items():
            if not val:
                exclude_columns_list.append(column)
        result = await (self._collection
                        .find(
                            search_params,
                            {c: 0 for c in exclude_columns_list}
                        )
                        .sort('word', self.__sort_map[sort])
                        .to_list(None))
        return result
