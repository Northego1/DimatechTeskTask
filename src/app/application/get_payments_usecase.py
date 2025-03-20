import uuid
from typing import Protocol

from app.application.dto import PaymentDto, TokenDto
from app.application.uow_protocol import UowProtocol
from app.domain.user import User
from core.exception import BaseError


class UserRepositoryProtocol(Protocol):
    async def get_user(
        self,
        *,
        user_id: uuid.UUID,
        include_accounts: bool = False,
        include_payments: bool = False,
    ) -> User | None: ...


class RepositoryProtocol(Protocol):
    user_repository: UserRepositoryProtocol


class SecurityProtocol(Protocol):
    def decode_and_verify_jwt(self, token: str) -> TokenDto | None: ...


class GetPaymentsUsecase:
    def __init__(
            self,
            uow: UowProtocol[RepositoryProtocol],
            security: SecurityProtocol,
    ) -> None:
        self.uow = uow
        self.security = security


    async def execute(self, access_token: str) -> list[PaymentDto]:
        if not (token_dto := self.security.decode_and_verify_jwt(access_token)):
            raise BaseError(status_code=401, detail="UNAUTHORIZED")

        async with self.uow.transaction() as repo:
            if not (user := await repo.user_repository.get_user(
                user_id=token_dto.person_id,
                include_accounts=True,
                include_payments=True,
            )):
                raise BaseError(status_code=404, detail="USER_NOT_FOUND")

            if user.accounts:
                return [
                    PaymentDto.from_domain(payment)
                    for account in user.accounts
                    for payment in account.payments if account.payments # type: ignore
                ]
            return []

