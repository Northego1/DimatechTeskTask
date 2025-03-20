import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.user import User


@dataclass
class Admin:
    id: uuid.UUID
    name: str
    email: str
    password: bytes
    users: list["User"] | None
