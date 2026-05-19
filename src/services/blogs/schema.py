from typing import Annotated, Optional
from pydantic import BaseModel, Field, ConfigDict


class BlogCreate(BaseModel):
    title: Annotated[str, Field(min_length=3, max_length=100)]
    content: Annotated[str, Field(min_length=10, max_length=200)]
    author: Annotated[str, Field(min_length=3, max_length=100)]
    image_base64: Optional[str] = None
    image_name: Optional[str] = None


class BlogUpdate(BaseModel):
    title: Annotated[str, Field(min_length=3, max_length=100)]
    content: Annotated[str, Field(min_length=10, max_length=200)]
    author: Annotated[str, Field(min_length=3, max_length=100)]
    image_base64: Optional[str] = None
    image_name: Optional[str] = None


class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str
    user_id: int
    image_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)