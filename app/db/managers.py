from typing import Any, Mapping

from sqlalchemy.orm import Session

from app.db import models


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
        # TODO: fix later
        except Exception:
            self._db.rollback()
        else:
            self._db.refresh(new_word)
        return new_word

    def get_word(self, word: str) -> Any:
        result = self._db.query(self._model).filter_by(word=word).first()
        return result

    def delete_word(self, word: str):
        result = self._db.query(self._model).filter_by(word=word).first()
        self._db.delete(result)
        self._db.commit()

    def get_words(
        self,
        sort: str,
        search_pattern: str | None = None,
        **columns: Mapping[str, bool],
    ):
        columns_list = [self._model.word]
        for column, val in columns.items():
            if val:
                columns_list.append(getattr(self._model, column))
        query = self._db.query(self._model).with_entities(*columns_list)
        if search_pattern:
            query = query.filter(
                self._model.word.ilike(f'%{search_pattern}%')
            )
        if sort:
            query = query.order_by(getattr(self._model.word, sort)())
        return query.all()
