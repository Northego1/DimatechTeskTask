import uuid
from typing import overload

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.admin import Admin
from app.infrastructure.models.admin_model import AdminModel
from app.infrastructure.models.user_model import UserModel


class AdminRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @overload
    async def get_admin(
        self,
        *,
        admin_id: uuid.UUID,
        include_users: bool = False,
        include_accounts: bool = False,
    ) -> Admin | None: ...
    @overload
    async def get_admin(
        self,
        *,
        email: str,
        include_users: bool = False,
        include_accounts: bool = False,
    ) -> Admin | None: ...

    async def get_admin(
        self,
        *,
        admin_id: uuid.UUID | None = None,
        email: str | None = None,
        include_users: bool = False,
        include_accounts: bool = False,
    ) -> Admin | None:
        if include_accounts:
            include_users = True

        query = select(AdminModel)
        if admin_id:
            query = query.where(AdminModel.id == admin_id)
        elif email:
            query = query.where(AdminModel.email == email)
        else:
            raise ValueError("Either user_id or email must be provided")

        if include_users:
            if include_accounts:
                query = query.options(
                    selectinload(AdminModel.users).selectinload(UserModel.accounts),
                )
            else:
                query = query.options(selectinload(AdminModel.users))

        result = await self.session.execute(query)

        if admin := result.scalars().first():
            return admin.to_domain(
                include_users=include_users,
                include_accounts=include_accounts,
            )
        return None
