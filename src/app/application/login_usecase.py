from typing import Protocol

from app.application.dto import LoginDto, TokenDto
from app.application.uow_protocol import UowProtocol
from app.domain.admin import Admin
from app.domain.user import User
from app.schemas.responses import Role
from core.config import JwtType
from core.exception import BaseError


class UserRepositoryProtocol(Protocol):
    async def get_user(
        self,
        *,
        email: str,
        include_accounts: bool = False,
        include_payments: bool = False,
    ) -> User | None: ...


class AdminRepositoryProtocol(Protocol):
    async def get_admin(
        self,
        *,
        email: str,
        include_users: bool = False,
        include_payments: bool = False,
    ) -> Admin | None: ...


class RepositoryProtocol(Protocol):
    user_repository: UserRepositoryProtocol
    admin_repository: AdminRepositoryProtocol


class SecurityProtocol(Protocol):
    def create_jwt(
        self,
        user: Admin | User,
        role: Role,
        jwt_type: JwtType,
    ) -> TokenDto: ...
    def check_password(self, correct_password: bytes, checkable_password: bytes) -> bool: ...


class LoginUsecase:
    def __init__(
        self,
        uow: UowProtocol[RepositoryProtocol],
        security: SecurityProtocol,
    ) -> None:
        self.uow = uow
        self.security = security

    async def _auth_user(self, email: str, password: str) -> User:
        async with self.uow.transaction() as repo:
            if not (user := await repo.user_repository.get_user(email=email)):
                raise BaseError(status_code=401, detail="Wrong email or password")

            if not self.security.check_password(
                correct_password=user.password,
                checkable_password=password.encode(),
            ):
                raise BaseError(status_code=401, detail="Wrong email or password")
            return user

    async def _auth_admin(self, email: str, password: str) -> Admin:
        async with self.uow.transaction() as repo:
            if not (admin := await repo.admin_repository.get_admin(email=email)):
                raise BaseError(status_code=401, detail="Wrong email or password")

            if not self.security.check_password(
                correct_password=admin.password,
                checkable_password=password.encode(),
            ):
                raise BaseError(status_code=401, detail="Wrong email or password")
            return admin

    async def execute(self, email: str, password: str, role: Role) -> LoginDto:
        if role == Role.USER:
            entity = await self._auth_user(email, password)
        elif role == Role.ADMIN:
            entity = await self._auth_admin(email, password)

        refresh_token = self.security.create_jwt(
            user=entity,
            role=role,
            jwt_type=JwtType.REFRESH,
        )
        access_token = self.security.create_jwt(
            user=entity,
            role=role,
            jwt_type=JwtType.ACCESS,
        )

        return LoginDto(
            refresh_jwt=refresh_token.token,
            access_jwt=access_token.token,
        )
