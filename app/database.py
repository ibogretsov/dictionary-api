from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app import config


engine = create_async_engine(
    config.get_settings().SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True
)
session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)
