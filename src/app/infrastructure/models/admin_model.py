import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DECIMAL, UUID, LargeBinary, String

from app.domain.admin import Admin
from core.database import Base

if TYPE_CHECKING:
    from app.infrastructure.models.user_model import UserModel


class AdminModel(Base):
    __tablename__ = "admins"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    email: Mapped[str] = mapped_column(String(128), index=True, unique=True)

    users: Mapped[list["UserModel"]] = relationship("UserModel", back_populates="admin")


    def to_domain(self, *, include_users: bool = False) -> Admin:
        return Admin(
            id=self.id,
            name=self.name,
            email=self.email,
            password=self.password,
            users=[user.to_domain() for user in self.users] if include_users else None,
        )
