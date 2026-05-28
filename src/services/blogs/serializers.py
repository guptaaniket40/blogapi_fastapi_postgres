from typing import Annotated, Optional
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class BlogCreateSerializer(BaseModel):
    title: Annotated[str, Field(min_length=3, max_length=100)]
    content: Annotated[str, Field(min_length=10, max_length=300)]
    author: Annotated[str, Field(min_length=3, max_length=100)]
    image_base64: Optional[str] = None
    image_name: Optional[str] = None


class BlogUpdateSerializer(BaseModel):
    title: Annotated[str, Field(min_length=3, max_length=100)]
    content: Annotated[str, Field(min_length=10, max_length=300)]
    author: Annotated[str, Field(min_length=3, max_length=100)]
    image_base64: Optional[str] = None
    image_name: Optional[str] = None


class BlogPatchSerializer(BaseModel):
    title: Optional[Annotated[str, Field(min_length=3, max_length=100)]] = None
    content: Optional[Annotated[str, Field(min_length=10, max_length=200)]] = None
    author: Optional[Annotated[str, Field(min_length=3, max_length=100)]] = None
    image_url: Optional[Annotated[str, Field(min_length=5, max_length=500)]] = None
    image_base64: Optional[str] = None
    image_name: Optional[str] = None


class BlogResponseSerializer(BaseModel):
    id: int
    title: str
    content: str
    author: str
    user_id: int
    image_url: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)