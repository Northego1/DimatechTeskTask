import uuid
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Payment:
    id: uuid.UUID
    account_id: uuid.UUID
    amount: Decimal
