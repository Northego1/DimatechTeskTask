import contextlib
import dataclasses
from typing import AsyncGenerator, Self

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure import repositories as repo
from core.database import DataBase
from core.exception import BaseError


@dataclasses.dataclass(slots=True)
class Repository:
    _conn: AsyncSession

    _user_repository: repo.UserRepository | None = None
    _admin_repository: repo.AdminRepository | None = None
    _payment_repository: repo.PaymentRepository | None = None
    _account_repository: repo.AccountRepository | None = None

    @property
    def user_repository(self: Self) -> repo.UserRepository:
        if not self._user_repository:
            self._user_repository = repo.UserRepository(self._conn)
        return self._user_repository

    @property
    def admin_repository(self: Self) -> repo.AdminRepository:
        if not self._admin_repository:
            self._admin_repository = repo.AdminRepository(self._conn)
        return self._admin_repository

    @property
    def payment_repository(self: Self) -> repo.PaymentRepository:
        if not self._payment_repository:
            self._payment_repository = repo.PaymentRepository(self._conn)
        return self._payment_repository

    @property
    def account_repository(self: Self) -> repo.AccountRepository:
        if not self._account_repository:
            self._account_repository = repo.AccountRepository(self._conn)
        return self._account_repository


class UnitOfWork:
    def __init__(self, db: DataBase) -> None:
        self.db = db

    @contextlib.asynccontextmanager
    async def transaction(self: Self) -> AsyncGenerator[Repository, None]:
        async for session in self.db.session_maker():
            session.begin()
            try:
                yield Repository(session)
                await session.commit()
            except BaseError as e:
                raise e from e
            except Exception as e:
                await session.rollback()
                raise BaseError from e
