from contextlib import asynccontextmanager
from typing import AsyncGenerator, Self

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from core.config import settings


class DataBase:
    def __init__(self: Self, url: str) -> None:
        self.engine = create_async_engine(url=url)
        self.async_session_maker = async_sessionmaker(self.engine, expire_on_commit=False)

    @asynccontextmanager
    async def connection(self: Self) -> AsyncGenerator[AsyncConnection, None]:
        async with self.engine.begin() as conn:
            yield conn

    async def session_maker(self: Self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            yield session


database = DataBase(settings.db.dsn)


class Base(DeclarativeBase):
    pass
