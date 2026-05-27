from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import get_db
from src.database.models import User
from src.database.jwt_config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)


PWD_CONTEXT = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

bearer_scheme = HTTPBearer()


class TokenHandler:

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode.update({
            "exp": expire,
            "type": "access"
        })

        return jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

    @classmethod
    def create_refresh_token(cls, data: dict) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )

        to_encode.update({
            "exp": expire,
            "type": "refresh"
        })

        return jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

    @classmethod
    def decode_token(cls, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )
        except Exception:
            raise HTTPException(
                detail="Invalid or expired token",
                status_code=status.HTTP_401_UNAUTHORIZED
            )


class PasswordHasher:

    @classmethod
    async def encrypt_password(
        cls,
        password: str
    ) -> str:
        return PWD_CONTEXT.hash(password)

    @classmethod
    async def check_password(
        cls,
        plain_password: str,
        hashed_password: str
    ) -> bool:
        return PWD_CONTEXT.verify(
            plain_password,
            hashed_password
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db_session: AsyncSession = Depends(get_db)
):
    token = credentials.credentials

    payload = TokenHandler.decode_token(token)

    user_id = payload.get("user_id")
    token_type = payload.get("type")

    if not user_id or token_type != "access":
        raise HTTPException(
            detail="Invalid token",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    result = await db_session.execute(
        select(User).where(User.id == int(user_id))
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            detail="User not found",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    return user