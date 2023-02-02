from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app import database
from app.db import managers


async def get_db_session() -> Generator:
    db = database.session()
    try:
        yield db
    finally:
        await db.close()


async def get_word_manager(
    db_session: Session = Depends(get_db_session)
) -> managers.WordDBManager:
    return managers.WordDBManager(db_session)
