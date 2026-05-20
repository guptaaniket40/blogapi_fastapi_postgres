from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import db
from src.services.auth.controller import AuthController
from src.services.auth.serializers import UserSignup, UserLogin,RefreshTokenSerializer


router = APIRouter(prefix="/auth",tags=["Auth"])


@router.post("/signup")
async def signup(
    user_data: UserSignup,
    db_session: AsyncSession = Depends(db.get_db)
):
    return await AuthController.signup(
        user_data=user_data,
        db=db_session
    )


@router.post("/login")
async def login(
    user_data: UserLogin,
    db_session: AsyncSession = Depends(db.get_db)
):
    return await AuthController.login(
        user_data=user_data,
        db=db_session
    )

@router.post("/refresh")
async def refresh_token(
    token_data: RefreshTokenSerializer
):
    return await AuthController.refresh_token(
        refresh_token=token_data.refresh_token
    )