import uuid
from typing import Protocol

from app.application.uow_protocol import UowProtocol
from app.domain.user import User
from core.exception import BaseError


class UserRepositoryProtocol(Protocol):
    async def add_user(self, user: User) -> uuid.UUID | None: ...


class RepositoryProtocol(Protocol):
    user_repository: UserRepositoryProtocol


class SecurityProtocol(Protocol):
    def hash_password(
        self,
        password: str,
    ) -> bytes: ...


class RegisterUserUsecase:
    def __init__(
        self,
        uow: UowProtocol[RepositoryProtocol],
        security: SecurityProtocol,
    ) -> None:
        self.uow = uow
        self.security = security

    async def execute(
        self,
        admin_id: uuid.UUID,
        email: str,
        password: str,
        username: str,
    ) -> None:
        hashed_password = self.security.hash_password(password)
        user = User(
            id=uuid.uuid4(),
            admin_id=admin_id,
            name=username,
            email=email,
            password=hashed_password,
        )
        async with self.uow.transaction() as repo:
            if not (user_id := await repo.user_repository.add_user(user)):
                raise BaseError(status_code=400, detail="User with this email already exists")
