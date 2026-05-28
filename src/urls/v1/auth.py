from fastapi import APIRouter

from src.services.auth.controller import AuthController
from src.services.auth.serializers import (
    UserSignup,
    UserLogin,
    RefreshTokenRequest
)

router= APIRouter(prefix="/auth",tags=["Auth"]
)


@router.post("/signup")
async def signup(
    request: UserSignup
):
    return await AuthController.signup(
        user_data=request
    )


@router.post("/login")
async def login(
    request: UserLogin
):
    return await AuthController.login(
        user_data=request
    )


@router.post("/refresh-token")
async def refresh_token(
    request: RefreshTokenRequest
):
    return await AuthController.refresh_token(
        refresh_token=request.refresh_token
    )