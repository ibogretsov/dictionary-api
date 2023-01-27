from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app import database
from app.db import managers


def get_db() -> Generator:
    db = database.session()
    try:
        yield db
    finally:
        db.close()


def get_word_manager(db: Session = Depends(get_db)) -> managers.WordDBManager:
    return managers.WordDBManager(db)
