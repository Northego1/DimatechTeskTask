import uuid
from enum import Enum

from pydantic import BaseModel

from app.application.dto import PaymentDto, UserDto
from core.config import JwtType


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


class LoginResponse(BaseModel):
    access_jwt: str
    jwt_type: JwtType = JwtType.ACCESS



class GetMeReponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    role: Role


class UserReponse(UserDto):
    ...


class PaymentResponse(PaymentDto):
    ...

