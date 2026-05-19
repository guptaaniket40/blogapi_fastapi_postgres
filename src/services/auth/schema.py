from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserSignup(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=100)]
    email: EmailStr
    password: Annotated[str, Field(min_length=6, max_length=72)]


class UserLogin(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=6, max_length=72)]


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)