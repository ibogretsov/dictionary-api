from typing import Any

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import constants
from app.db import models
from app.exceptions import WordNotFoundError


class WordDBManager:

    def __init__(self, db: Session) -> None:
        self._db = db
        self._model = models.Word

    def insert_word_info(self, word_details: dict[str, Any]):
        """Just insert word and return result of this insert."""
        new_word = self._model(**word_details)
        self._db.add(new_word)
        try:
            self._db.commit()
        except IntegrityError as exc:  # noqa
            self._db.rollback()
        else:
            self._db.refresh(new_word)
        return new_word

    def get_word(self, word: str) -> Any:
        result = self._db.query(self._model).filter_by(word=word).one_or_none()
        if not result:
            raise WordNotFoundError(constants.WORD_NOT_FOUND.format(word=word))
        return result

    def delete_word(self, word: str):
        result = self.get_word(word)
        self._db.delete(result)
        self._db.commit()

    def get_words(
        self,
        sort: str,
        search_pattern: str | None = None,
        **columns: bool,
    ) -> list[Any]:
        columns_list = [self._model.word]
        for column, to_return in columns.items():
            if to_return:
                columns_list.append(getattr(self._model, column))
        query = self._db.query(self._model).with_entities(*columns_list)
        if search_pattern:
            query = query.filter(
                self._model.word.ilike(f'%{search_pattern}%')
            )
        if sort:
            query = query.order_by(getattr(self._model.word, sort)())
        return query.all()
