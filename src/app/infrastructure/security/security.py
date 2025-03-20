import uuid
from datetime import UTC, datetime, timedelta
from typing import Self

import bcrypt
import jwt

from app.application.dto import AdminDto, TokenDto, UserDto
from app.domain.admin import Admin
from app.domain.user import User
from app.schemas.responses import Role
from core.config import JwtType, settings


class Security:
    def create_jwt(
            self: Self,
            user: Admin | User,
            role: Role,
            jwt_type: JwtType,
    ) -> TokenDto:
        """creating jwt token, extending jti, token_type, expire"""
        expire = 3600 if jwt_type == JwtType.REFRESH else 10
        expire_at = (datetime.now(UTC) + timedelta(minutes=expire))

        payload = {
            "user_id": str(user.id),
            "role": Role,
            "exp": expire_at.timestamp(),
        }

        token = jwt.encode(
            payload=payload,
            key=settings.jwt.PRIVATE_KEY,
            algorithm=settings.jwt.ALGORITHM,
        )
        return TokenDto(
            token=token,
            person_id=user.id,
            role=role,
            exp=expire_at,
        )


    def decode_and_verify_jwt(self: Self, token: str) -> TokenDto | None:
        """ returns None if token is invalid"""
        try:
            payload = jwt.decode(
                token,
                key=settings.jwt.PUBLIC_KEY,
                algorithms=[settings.jwt.ALGORITHM],
            )
            return TokenDto(
                person_id=payload["user_id"],
                token=token,
                exp=datetime.fromtimestamp(int(payload["exp"]), tz=UTC),
                role=Role(payload["role"]),
            )
        except jwt.exceptions.PyJWTError:
            return None


    def hash_password(
            self: Self,
            password: str,
    ) -> bytes:
        return bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt(),
        )

    def check_password(
            self: Self,
            correct_password: bytes,
            checkable_password: bytes,
    ) -> bool:
        return bcrypt.checkpw(
            checkable_password,
            correct_password,
        )
