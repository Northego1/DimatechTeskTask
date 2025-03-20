import uuid
from decimal import Decimal
from typing import Protocol

from app.application.uow_protocol import UowProtocol
from app.domain.account import Account
from app.domain.payment import Payment
from app.domain.user import User
from app.schemas.requests import PaymentRequest
from core.exception import BaseError


class UserRepositoryProtocol(Protocol):
    async def get_user(
        self,
        *,
        user_id: uuid.UUID,
        include_accounts: bool = False,
        include_payments: bool = False,
    ) -> User | None: ...


class AccountRepositoryProtocol(Protocol):
    async def get_account(
        self, account_id: uuid.UUID, *, include_payments: bool = False
    ) -> Account | None: ...
    async def add_account(self, account: Account) -> uuid.UUID | None: ...


class PaymentRepositoryProtocol(Protocol):
    async def add_payment(self, payment: Payment) -> uuid.UUID | None: ...


class RepositoryProtocol(Protocol):
    user_repository: UserRepositoryProtocol
    account_repository: AccountRepositoryProtocol
    payment_repository: PaymentRepositoryProtocol


class PaymentUsecase:
    def __init__(
        self,
        uow: UowProtocol[RepositoryProtocol],
    ) -> None:
        self.uow = uow

    async def execute(self, payments_data: PaymentRequest) -> None:
        async with self.uow.transaction() as repo:
            if not (
                user := await repo.user_repository.get_user(
                    user_id=payments_data.user_id,
                )
            ):
                raise BaseError(status_code=404, detail="User not found")

            payment = Payment(
                id=payments_data.transaction_id,
                amount=Decimal(payments_data.amount),
                account_id=payments_data.account_id,
            )

            if not (
                account := await repo.account_repository.get_account(
                    account_id=payments_data.account_id,
                )
            ):
                account = Account(
                    id=payments_data.account_id,
                    user_id=payments_data.user_id,
                    balance=Decimal(0),
                    payments=[],
                )
                account.deposit(payment)
                if not (_ := await repo.account_repository.add_account(account)):
                    raise BaseError(status_code=400, detail="Payment already exists")
            else:
                account.deposit(payment)
                if not (_ := await repo.payment_repository.add_payment(payment)):
                    raise BaseError(status_code=400, detail="Payment already exists")
