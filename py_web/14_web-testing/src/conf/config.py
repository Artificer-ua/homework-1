from typing import Any

from pydantic import ConfigDict, EmailStr, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = ""

    SECRET_KEY_JWT: str = "1234567890"
    ALGORITHM: str = "HS256"
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: EmailStr = "example@mail.com"
    MAIL_PORT: int = 0
    MAIL_SERVER: str = ""
    REDIS_DOMAIN: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    CLOUDINARY_NAME: str = ""
    CLOUDINARY_API_KEY: int = 0
    CLOUDINARY_API_SECRET: str = ""

    @field_validator("ALGORITHM")
    @classmethod
    def validate(cls, value: Any):
        if value not in ["HS256", "HS512"]:
            raise ValueError("Algorithm must be HS256 or HS512")
        return value

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )  # noqa


config = Settings()
