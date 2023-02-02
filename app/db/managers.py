from typing import Any

from sqlalchemy import future
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app import constants
from app.db import models
from app.exceptions import WordNotFoundError


class WordDBManager:

    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session = db_session
        self._model = models.Word

    async def insert_word_info(self, word_details: dict[str, Any]):
        """Just insert word and return result of this insert."""
        new_word = self._model(**word_details)
        self._db_session.add(new_word)
        try:
            await self._db_session.commit()
        except IntegrityError as exc:  # noqa
            await self._db_session.rollback()
        else:
            await self._db_session.refresh(new_word)
        return new_word

    async def get_word(self, word: str) -> models.Word:
        query = future.select(self._model).where(self._model.word == word)
        result: models.Word | None = await self._db_session.scalar(query)
        if not result:
            raise WordNotFoundError(constants.WORD_NOT_FOUND.format(word=word))
        return result

    async def delete_word(self, word: str) -> None:
        result = await self.get_word(word)
        await self._db_session.delete(result)
        await self._db_session.commit()

    async def get_words(
        self,
        sort: str,
        search_pattern: str | None = None,
        **columns: bool,
    ) -> list[Any]:
        columns_list = [self._model.word]
        for column, to_return in columns.items():
            if to_return:
                columns_list.append(getattr(self._model, column))
        query = future.select(*columns_list)
        if search_pattern:
            query = query.filter(
                self._model.word.ilike(f'%{search_pattern}%')
            )
        if sort:
            query = query.order_by(getattr(self._model.word, sort)())
        result: ChunkedIteratorResult = await self._db_session.execute(query)
        return result.all()
