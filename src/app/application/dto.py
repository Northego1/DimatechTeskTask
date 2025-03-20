import email
import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Self

from app.domain.account import Account
from app.domain.payment import Payment
from app.domain.user import User
from app.schemas.responses import Role


@dataclass
class LoginDto:
    refresh_jwt: str
    access_jwt: str


@dataclass
class AdminDto:
    id: uuid.UUID
    name: str
    email: str


@dataclass
class AccountDto:
    id: uuid.UUID
    balance: Decimal

    @classmethod
    def from_domain(cls, account: Account) -> Self:
        return cls(
            id=account.id,
            balance=account.balance,
        )


@dataclass
class UserDto:
    id: uuid.UUID
    username: str
    email: str
    accounts: list[AccountDto] | None = None

    @classmethod
    def from_domain(cls, user: User) -> Self:
        return cls(
            id=user.id,
            username=user.name,
            email=user.email,
            accounts=[AccountDto.from_domain(account) for account in user.accounts]
            if user.accounts
            else None,
        )


@dataclass
class PaymentDto:
    id: uuid.UUID
    account_id: uuid.UUID
    amount: Decimal

    @classmethod
    def from_domain(cls, payment: Payment) -> Self:
        return cls(
            id=payment.id,
            account_id=payment.account_id,
            amount=payment.amount,
        )


@dataclass
class TokenDto:
    token: str
    person_id: uuid.UUID
    role: Role
    exp: datetime


@dataclass
class PaymentData:
    transaction_id: uuid.UUID
    account_id: uuid.UUID
    user_id: uuid.UUID
    amount: float
