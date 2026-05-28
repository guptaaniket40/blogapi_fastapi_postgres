from fastapi import HTTPException, status

from src.services.auth.schema import UserSchema
from src.services.auth.serializers import UserSignup, UserLogin, UserResponse
from src.utils.response import success_response
from src.utils.security import PasswordHasher, TokenHandler


class AuthController:

    @classmethod
    async def signup(
        cls,
        user_data: UserSignup
    ):
        existing_user = await UserSchema.get_user_data(
            email=user_data.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        user_data.password = await PasswordHasher.encrypt_password(
            user_data.password
        )

        new_user = await UserSchema.create_user(
            request=user_data
        )

        return success_response(
            "User registered successfully",
            UserResponse.model_validate(new_user).model_dump(mode="json")
        )

    @classmethod
    async def login(
        cls,
        user_data: UserLogin
    ):
        user = await UserSchema.get_user_data(
            email=user_data.email
        )

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