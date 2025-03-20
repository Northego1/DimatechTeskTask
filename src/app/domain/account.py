import uuid
from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING

from core.exception import BaseError

if TYPE_CHECKING:
    from app.domain.payment import Payment

@dataclass
class Account:
    id: uuid.UUID
    user_id: uuid.UUID
    balance: Decimal
    payments: list["Payment"] | None


    def deposit(self, payment: "Payment") -> None:
        if self.id != payment.account_id:
            raise BaseError

        self.balance += payment.amount

        if self.payments is None:
            self.payments = []

        self.payments.append(payment)



