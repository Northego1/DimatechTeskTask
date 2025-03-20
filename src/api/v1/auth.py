import uuid
from typing import Protocol

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from app.application.dto import AdminDto, LoginDto
from app.schemas import requests, responses
from core.config import JwtType
from core.container import Container
from core.exception import BaseError

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


class LoginUsecaseProtocol(Protocol):
    async def execute(self, email: str, password: str) -> LoginDto: ...


class CreateUserUsecaseProtocol(Protocol):
    async def execute(
            self, admin_id: uuid.UUID,
            email: str, password: str, username: str) -> None: ...


class GetMeUsecaseProtocol(Protocol):
    async def get_admin(self, token: str) -> AdminDto: ...


@router.post("/login", status_code=status.HTTP_200_OK)
@inject
async def login(
    login_request: requests.LoginUserRequest,
    response: Response,
    login_uc: LoginUsecaseProtocol = Depends(Provide[Container.login_usecase]),
) -> responses.LoginResponse:
    try:
        login_dto = await login_uc.execute(
            email=login_request.email,
            password=login_request.password,
        )
        response.set_cookie(
            JwtType.REFRESH.value,
            login_dto.refresh_jwt,
            httponly=True,
            samesite="strict",
            max_age=3600,
        )
        return responses.LoginResponse(access_jwt=login_dto.access_jwt)

    except BaseError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        ) from e


@router.post("/create_user", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def create_user(
    create_user_request: requests.CreateUserRequest,
    request: Request,
    getme_uc: GetMeUsecaseProtocol = Depends(Provide[Container.getme_usecase]),
    create_user_uc: CreateUserUsecaseProtocol = Depends(Provide[Container.register_user_usecase]),
) -> None:
    try:
        if access_token_header := request.headers.get("Authorization"):
            if len(splited_token := access_token_header.split()) == 2:
                admin = await getme_uc.get_admin(token=splited_token[1])
                await create_user_uc.execute(
                    admin_id=admin.id,
                    username=create_user_request.username,
                    email=create_user_request.email,
                    password=create_user_request.password,
                )
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except BaseError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        ) from e
