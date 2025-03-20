import uuid
from typing import Protocol

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.application import dto
from app.schemas import requests
from core.container import Container
from core.exception import BaseError

router = APIRouter(
    prefix="/port",
    tags=["hew"],
)

class GetPaymentsUsecaseProtocol(Protocol):
    async def execute(self, user_id: uuid.UUID) -> list[dto.PaymentDto]: ...


class GetAccountsUsecaseProtocol(Protocol):
    async def execute(self, user_id: uuid.UUID) -> list[dto.AccountDto]: ...


class GetMeUsecaseProtocol(Protocol):
    async def get_admin(self, token: str) -> dto.AdminDto: ...

    async def get_user(self, token: str) -> dto.UserDto: ...


class GetUsersUsecaseProtocol(Protocol):
    async def execute(self, admin_id: uuid.UUID) -> list[dto.UserDto]: ...


class PaymentUsecaseProtocol(Protocol):
    async def execute(self, payments_data: requests.PaymentData) -> dto.PaymentDto: ...


class PaymentVerifyUsecase(Protocol):
    async def execute(self, signature: str, data_str: str) -> None: ...


@router.get("/accounts", status_code=status.HTTP_200_OK)
async def get_accounts(
    request: Request,
    getme_uc: GetMeUsecaseProtocol = Depends(Provide[Container.getme_usecase]),
    get_accounts_uc: GetAccountsUsecaseProtocol = Depends(Provide[Container.get_accounts_usecase]),
)  -> list[dto.AccountDto]:
    try:
        if access_token_header := request.headers.get("Authorization"):
            if len(splited_token := access_token_header.split()) == 2:
                user = await getme_uc.get_user(token=splited_token[1])
                return await get_accounts_uc.execute(user_id=user.id)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except BaseError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        ) from e


@router.get("/payments", status_code=status.HTTP_200_OK)
@inject
async def get_payments(
    request: Request,
    getme_uc: GetMeUsecaseProtocol = Depends(Provide[Container.getme_usecase]),
    get_payments_uc: GetPaymentsUsecaseProtocol = Depends(Provide[Container.get_payments_usecase]),
)  -> list[dto.PaymentDto]:
    try:
        if access_token_header := request.headers.get("Authorization"):
            if len(splited_token := access_token_header.split()) == 2:
                user = await getme_uc.get_user(token=splited_token[1])
                return await get_payments_uc.execute(user_id=user.id)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except BaseError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        ) from e


@router.get("/users", status_code=status.HTTP_200_OK)
@inject
async def get_users(
    request: Request,
    getme_uc: GetMeUsecaseProtocol = Depends(Provide[Container.getme_usecase]),
    get_users_uc: GetUsersUsecaseProtocol = Depends(Provide[Container.get_users_usecase]),
) -> list[dto.UserDto]:
    try:
        if access_token_header := request.headers.get("Authorization"):
            if len(splited_token := access_token_header.split()) == 2:
                admin = await getme_uc.get_admin(token=splited_token[1])
                return await get_users_uc.execute(admin_id=admin.id)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except BaseError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        ) from e


@router.post("/payment", status_code=204)
@inject
async def payment(
    payment_request: requests.PaymentRequest,
    verify_uc: PaymentVerifyUsecase = Depends(Provide[Container.payment_verify_usecase]),
    payment_uc: PaymentUsecaseProtocol = Depends(Provide[Container.payment_usecase]),
) -> None:
    try:
        data = payment_request.model_dump(exclude={"signature",})
        data_str = "".join(str(elem) for elem in data.values())
        await verify_uc.execute(
            signature=payment_request.signature,
            data_str=data_str,
        )
        await payment_uc.execute(payments_data=payment_request)
    except BaseError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        ) from e







