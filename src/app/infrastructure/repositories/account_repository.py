import uuid

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from app.domain.account import Account
from app.infrastructure.models.account_model import AccountModel


class AccountRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_account(
            self,
            account_id: uuid.UUID,
            *,
            include_payments: bool = False,
    ) -> Account | None:
        query = (
            select(AccountModel)
            .where(AccountModel.id == account_id)
            .with_for_update()
        )
        if include_payments:
            query = query.options(selectinload(AccountModel.payments))

        result = await self.session.execute(query)

        if account := result.scalars().first():
            return account.to_domain(include_payments=include_payments)
        return None


    async def add_account(self, account: Account) -> uuid.UUID | None:
        account_model = AccountModel.from_domain(account)
        self.session.add(account_model)
        try:
            await self.session.flush()
        except IntegrityError:
            return None
        return account_model.id





