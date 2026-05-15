
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import get_db
from src.services.auth.schema import UserSignup, UserLogin
from src.services.auth import controller

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup")
async def signup(
    user_data: UserSignup,
    db: AsyncSession = Depends(get_db)
):
    return await controller.signup(user_data, db)


@router.post("/login")
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    return await controller.login(user_data, db)