import uuid
from decimal import Decimal

from core.exception import BaseError


class Payment:
    def __init__(
        self,
        id: uuid.UUID,
        account_id: uuid.UUID,
        amount: Decimal,
    ) -> None:
        self.id = id
        self.account_id = account_id
        self._amount = amount

    @property
    def amount(self) -> Decimal:
        return self._amount

    @amount.setter
    def amount(self, value: Decimal) -> None:
        if value <= 0:
            raise BaseError(
                status_code=400,
                detail="amount must be greate then 0",
            )
