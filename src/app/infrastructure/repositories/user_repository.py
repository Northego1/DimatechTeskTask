import uuid
from typing import overload

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.user import User
from app.infrastructure.models.account_model import AccountModel
from app.infrastructure.models.user_model import UserModel


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @overload
    async def get_user(
        self,
        *,
        user_id: uuid.UUID,
        include_accounts: bool = False,
        include_payments: bool = False,
    ) -> User | None: ...
    @overload
    async def get_user(
        self,
        *,
        email: str,
        include_accounts: bool = False,
        include_payments: bool = False,
    ) -> User | None: ...

    async def get_user(
        self,
        *,
        user_id: uuid.UUID | None = None,
        email: str | None = None,
        include_accounts: bool = False,
        include_payments: bool = False,
    ) -> User | None:
        if include_payments:
            include_accounts = True

        query = select(UserModel)
        if user_id:
            query = query.where(UserModel.id == user_id)
        elif email:
            query = query.where(UserModel.email == email)
        else:
            raise ValueError("Either user_id or email must be provided")

        if include_accounts:
            if include_payments:
                query = query.options(
                    selectinload(UserModel.accounts).selectinload(AccountModel.payments),
                )
            else:
                query = query.options(selectinload(UserModel.accounts))

        result = await self.session.execute(query)

        if user := result.scalars().first():
            return user.to_domain(
                include_accounts=include_accounts,
                include_payments=include_payments,
            )
        return None

    async def add_user(self, user: User) -> uuid.UUID | None:
        user_model = UserModel.from_domain(user)
        self.session.add(user_model)
        try:
            await self.session.flush()
        except IntegrityError:
            return None
        return user_model.id
