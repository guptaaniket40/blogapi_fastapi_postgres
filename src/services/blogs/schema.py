from pydantic import BaseModel, constr, ConfigDict


class BlogCreate(BaseModel):
    title: constr(min_length=3, max_length=200)
    content: constr(min_length=10)
    author: constr(min_length=2, max_length=100)


class BlogUpdate(BaseModel):
    title: constr(min_length=3, max_length=200)
    content: constr(min_length=10)
    author: constr(min_length=2, max_length=100)


class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)