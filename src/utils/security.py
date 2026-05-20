from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.config import Config
from src.database.db_config import db
from src.database.models import User


PWD_CONTEXT = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


class TokenHandler:

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode.update({
            "exp": expire,
            "type": "access"
        })

        return jwt.encode(
            to_encode,
            Config.SECRET_KEY,
            algorithm=Config.ALGORITHM
        )

    @classmethod
    def create_refresh_token(cls, data: dict) -> str:
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            days=Config.REFRESH_TOKEN_EXPIRE_DAYS
        )

        to_encode.update({
            "exp": expire,
            "type": "refresh"
        })

        return jwt.encode(
            to_encode,
            Config.SECRET_KEY,
            algorithm=Config.ALGORITHM
        )

    @classmethod
    def decode_token(cls, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                Config.SECRET_KEY,
                algorithms=[Config.ALGORITHM]
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
    token: str = Depends(oauth2_scheme),
    db_session: AsyncSession = Depends(db.get_db)
):
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