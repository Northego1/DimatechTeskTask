import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DECIMAL, UUID

from app.domain.account import Account
from core.database import Base

if TYPE_CHECKING:
    from app.infrastructure.models.payment_model import PaymentModel
    from app.infrastructure.models.user_model import UserModel



class AccountModel(Base):
    __tablename__ = "accounts"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"), nullable=False)
    balance: Mapped[Decimal] = mapped_column(DECIMAL, default=0, nullable=False)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="accounts")
    payments: Mapped[list["PaymentModel"]] = relationship("PaymentModel", back_populates="account")


    def to_domain(self, *, include_payments: bool = False) -> Account:
        return Account(
            id=self.id,
            user_id=self.user_id,
            balance=self.balance,
            payments=[payment.to_domain() for payment in self.payments] if include_payments else None,
        )


    @classmethod
    def from_domain(cls, account: Account) -> "AccountModel":
        return cls(
            id=account.id,
            user_id=account.user_id,
            balance=account.balance,
            payments=[
                PaymentModel.from_domain(payment) for payment in account.payments
                ] if account.payments else [],
        )
