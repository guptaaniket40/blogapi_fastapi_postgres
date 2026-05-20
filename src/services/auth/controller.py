from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.services.auth.serializers import UserSignup, UserLogin, UserResponse
from src.utils.response import success_response
from src.utils.security import PasswordHasher, TokenHandler


class AuthController:

    @classmethod
    async def signup(
        cls,
        user_data: UserSignup,
        db: AsyncSession
    ):
        result = await db.execute(
            select(User).where(User.email == user_data.email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        hashed_password = await PasswordHasher.encrypt_password(
            user_data.password
        )

        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hashed_password
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return success_response(
            "User registered successfully",
            UserResponse.model_validate(new_user).model_dump(mode="json")
        )

    @classmethod
    async def login(
        cls,
        user_data: UserLogin,
        db: AsyncSession
    ):
        result = await db.execute(
            select(User).where(User.email == user_data.email)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        valid_password = await PasswordHasher.check_password(
            user_data.password,
            user.password
        )

        if not valid_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        token_data = {
            "user_id": user.id,
            "email": user.email
        }

        access_token = TokenHandler.create_access_token(data=token_data)
        refresh_token = TokenHandler.create_refresh_token(data=token_data)

        return success_response(
            "Login successful",
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }
        )
    

    @classmethod
    async def refresh_token(
        cls,
        refresh_token: str
    ):
        payload = TokenHandler.decode_token(refresh_token)

        token_type = payload.get("type")

        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        token_data = {
            "user_id": payload.get("user_id"),
            "email": payload.get("email")
        }

        new_access_token = TokenHandler.create_access_token(
            data=token_data
        )

        return success_response(
            "Access token refreshed successfully",
            {
                "access_token": new_access_token,
                "token_type": "bearer"
            }
        )       