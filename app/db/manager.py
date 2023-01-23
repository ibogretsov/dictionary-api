from typing import Any, Mapping

import pymongo
from pymongo.database import Database
from pymongo.results import DeleteResult
from pymongo.results import InsertOneResult

from app import constants


class WordDBManager:

    __sort_map = {
        constants.SortTypeEnum.asc.value: pymongo.ASCENDING,
        constants.SortTypeEnum.desc.value: pymongo.DESCENDING
    }

    def __init__(self, db: Database) -> None:
        self._db = db
        self._collection = self._db.words

    def insert_word_info(
            self,
            word_details: dict[str, Any]
    ) -> InsertOneResult:
        """Just insert word and return result of this insert."""
        result: InsertOneResult = self._collection.insert_one(word_details)
        return result

    def get_word(self, word: str) -> Any:
        result = self._collection.find_one({'word': word})
        return result

    def delete_word(self, word: str) -> DeleteResult:
        result: DeleteResult = self._collection.delete_one({'word': word})
        return result

    def get_words(
        self,
        sort: str,
        search_pattern: str | None = None,
        **columns: Mapping[str, bool],
    ):
        search_params: dict[str, dict[str, str]] = {}
        # if partial filtering exists and we have search patter. Filter
        # words by this pattern. Add option 'i' to make search case-insensitive
        if search_pattern:
            search_params = {
                'word': {
                    '$regex': search_pattern,
                    '$options': 'i'
                }
            }
        # https://www.mongodb.com/docs/manual/tutorial/project-fields-from-query-results/#suppress-_id-field  # noqa
        # by default return only words
        columns_map: dict[str, int] = {'word': 1}
        for column, val in columns.items():
            if val:
                columns_map[column] = 1
        result = (self._collection
                      .find(search_params, columns_map)
                      .sort('word', self.__sort_map[sort]))
        return list(result)
