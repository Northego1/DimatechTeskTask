import uuid
from typing import Protocol

from app.application.dto import TokenDto, UserDto
from app.application.uow_protocol import UowProtocol
from app.domain.admin import Admin
from core.exception import BaseError


class AdminRepositoryProtocol(Protocol):
    async def get_admin(
        self,
        *,
        admin_id: uuid.UUID,
        include_users: bool = False,
        include_accounts: bool = False,
    ) -> Admin | None: ...


class RepositoryProtocol(Protocol):
    admin_repository: AdminRepositoryProtocol


class SecurityProtocol(Protocol):
    def decode_and_verify_jwt(self, token: str) -> TokenDto | None: ...


class GetUsersUsecase:
    def __init__(
        self,
        uow: UowProtocol[RepositoryProtocol],
        security: SecurityProtocol,
    ) -> None:
        self.uow = uow
        self.security = security

    async def execute(self, access_token: str) -> list[UserDto]:
        if not (token_dto := self.security.decode_and_verify_jwt(access_token)):
            raise BaseError(status_code=401, detail="UNAUTHORIZED")

        async with self.uow.transaction() as repo:
            if not (
                admin := await repo.admin_repository.get_admin(
                    admin_id=token_dto.person_id,
                    include_users=True,
                    include_accounts=True,
                )
            ):
                raise BaseError
            return [UserDto.from_domain(user) for user in admin.users] if admin.users else []
