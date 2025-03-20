import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.account import Account


@dataclass
class User:
    id: uuid.UUID
    name: str
    email: str
    password: bytes
    admin_id: uuid.UUID
    accounts: list["Account"] | None = None

    def add_account(self, account: "Account") -> None:
        if not self.accounts:
            self.accounts = []

        self.accounts.append(account)
