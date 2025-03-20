import uuid
from enum import Enum

from pydantic import BaseModel

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
