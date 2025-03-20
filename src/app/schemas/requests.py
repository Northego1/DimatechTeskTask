import uuid
from pydantic import BaseModel, EmailStr

from app.application.dto import PaymentData
from app.schemas.responses import Role


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str
    role: Role


class PaymentRequest(BaseModel):
    transaction_id: uuid.UUID
    account_id: uuid.UUID
    user_id: uuid.UUID
    amount: float
    signature: str
