import uuid
from typing import Protocol

from app.application.dto import AdminDto, TokenDto, UserDto
from app.application.uow_protocol import UowProtocol
from app.domain.admin import Admin
from app.domain.user import User
from core.exception import BaseError


class UserRepositoryProtocol(Protocol):
        async def get_user(
            self, *, user_id: uuid.UUID,
            include_accounts: bool = False,
            include_payments: bool = False,
    ) -> User | None: ...


class AdminRepositoryProtocol(Protocol):
        async def get_admin(
            self, *, admin_id: uuid.UUID,
            include_users: bool = False,
            include_payments: bool = False,
    ) -> Admin | None: ...


class RepositoryProtocol(Protocol):
    user_repository: UserRepositoryProtocol
    admin_repository: AdminRepositoryProtocol


class SecurityProtocol(Protocol):
    def decode_and_verify_jwt(self, token: str) -> TokenDto | None: ...


class GetMeUsecase:
    def __init__(
            self,
            uow: UowProtocol[RepositoryProtocol],
            security: SecurityProtocol,
    ) -> None:
        self.uow = uow
        self.security = security


    async def get_admin(self, token: str) -> AdminDto:
        if not (token_dto := self.security.decode_and_verify_jwt(token)):
            raise BaseError(status_code=401, detail="UNAUTHORIZED")

        async with self.uow.transaction() as repo:
            admin = await repo.admin_repository.get_admin(
                admin_id=token_dto.person_id)
            if not admin:
                raise BaseError(status_code=404, detail="NOT_FOUND")
            return AdminDto(
                id=admin.id,
                name=admin.name,
                email=admin.email,
            )


    async def get_user(self, token: str) -> UserDto:
        if not (token_dto := self.security.decode_and_verify_jwt(token)):
            raise BaseError(status_code=401, detail="UNAUTHORIZED")

        async with self.uow.transaction() as repo:
            user = await repo.user_repository.get_user(
                user_id=token_dto.person_id,
            )
            if not user:
                raise BaseError(status_code=404, detail="NOT_FOUND")
            return UserDto(
                id=user.id,
                username=user.name,
                email=user.email,
            )
