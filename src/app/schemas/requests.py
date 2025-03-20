from pydantic import BaseModel, EmailStr

from app.application.dto import PaymentData


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str
    is_admin: bool



class PaymentRequest(PaymentData):
    signature: str

