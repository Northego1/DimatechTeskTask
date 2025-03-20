import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DECIMAL, UUID

from app.domain.payment import Payment
from core.database import Base

if TYPE_CHECKING:
    from app.infrastructure.models.account_model import AccountModel


class PaymentModel(Base):
    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    account_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("accounts.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)

    account: Mapped["AccountModel"] = relationship("AccountModel", back_populates="payments")


    def to_domain(self) -> Payment:
        return Payment(
            id=self.id,
            account_id=self.account_id,
            amount=self.amount,
        )


    @classmethod
    def from_domain(cls, payment: Payment) -> "PaymentModel":
        return cls(
            id=payment.id,
            account_id=payment.account_id,
            amount=payment.amount,
        )
