from enum import Enum
from pathlib import Path
from typing import Self

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class JwtType(str, Enum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class CustomSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class JwtSettings(CustomSettings):
    PRIVATE_KEY: str = (BASE_DIR / "jwt_certs" / "jwt-private.pem").read_text()

    PUBLIC_KEY: str = (BASE_DIR / "jwt_certs" / "jwt-public.pem").read_text()

    ALGORITHM: str = "RS256"


class TransactionSettings(CustomSettings):
    TRANSACTION_KEY: str = "HELLO"


class DataBaseSettings(CustomSettings):
    DB_USER: str = "postgres"
    DB_PASS: str = "0420"
    DB_NAME: str = "account"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"

    @property
    def dsn(self: Self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


class Settings:
    def __init__(self: Self) -> None:
        self.db = DataBaseSettings()
        self.jwt = JwtSettings()
        self.ts = TransactionSettings()


settings = Settings()
