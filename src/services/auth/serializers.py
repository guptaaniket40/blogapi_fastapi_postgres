from typing import Annotated, Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserSignup(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=100)]
    email: EmailStr
    password: Annotated[str, Field(min_length=6, max_length=72)]

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=6, max_length=72)]


class RefreshTokenSerializer(BaseModel):
    refresh_token: str    


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UserTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"