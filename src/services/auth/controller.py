from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.services.auth.schema import UserSignup, UserLogin
from src.services.auth.serializers import serialize_user
from src.utils.response import success_response
from src.utils.security import hash_password, verify_password, create_access_token


async def signup(user_data: UserSignup, db: AsyncSession):
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return success_response(
        "User registered successfully",
        serialize_user(new_user)
    )


async def login(user_data: UserLogin, db: AsyncSession):
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "user_id": user.id,
            "email": user.email
        }
    )

    return success_response(
        "Login successful",
        {
            "access_token": access_token,
            "token_type": "bearer"
        }
    )