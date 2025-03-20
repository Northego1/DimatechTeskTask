import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import UUID, LargeBinary, String

from app.domain.user import User
from app.infrastructure.models.account_model import AccountModel
from core.database import Base

if TYPE_CHECKING:
    from app.infrastructure.models.admin_model import AdminModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    admin_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("admins.id"), nullable=False)

    accounts: Mapped[list[AccountModel]] = relationship(
        "app.infrastructure.models.account_model.AccountModel",
        back_populates="user",
    )
    admin: Mapped["AdminModel"] = relationship(
        "app.infrastructure.models.admin_model.AdminModel",
        back_populates="users",
    )

    def to_domain(
        self,
        *,
        include_accounts: bool = False,
        include_payments: bool = False,
    ) -> User:
        return User(
            id=self.id,
            name=self.name,
            email=self.email,
            password=self.password,
            admin_id=self.admin_id,
            accounts=[
                account.to_domain(include_payments=include_payments) for account in self.accounts
            ]
            if include_accounts
            else None,
        )

    @classmethod
    def from_domain(cls, user: User) -> "UserModel":
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.password,
            admin_id=user.admin_id,
            accounts=[AccountModel.from_domain(account) for account in user.accounts]
            if user.accounts
            else [],
        )
