from pydantic import BaseModel, EmailStr, constr, ConfigDict


class UserSignup(BaseModel):
    name: constr(min_length=3, max_length=100)
    email: EmailStr
    password: constr(min_length=6, max_length=72)


class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=72)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)