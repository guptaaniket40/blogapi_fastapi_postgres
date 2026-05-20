from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import db
from src.database.models import User
from src.services.blogs.serializers import (
    BlogCreateSerializer,
    BlogUpdateSerializer,
    BlogPatchSerializer
)
from src.services.blogs.controller import BlogController
from src.utils.security import get_current_user


router = APIRouter(prefix="/blogs", tags=["Blogs"])


@router.post("/")
async def create_blog(
    blog_data: BlogCreateSerializer,
    db_session: AsyncSession = Depends(db.get_db),
    current_user: User = Depends(get_current_user)
):
    return await BlogController.create_blog(
        blog_data=blog_data,
        db=db_session,
        current_user=current_user
    )


@router.get("/")
async def get_all_blogs(
    db_session: AsyncSession = Depends(db.get_db)
):
    return await BlogController.get_all_blogs(
        db=db_session
    )


@router.get("/{blog_id}")
async def get_blog_by_id(
    blog_id: int,
    db_session: AsyncSession = Depends(db.get_db)
):
    return await BlogController.get_blog_by_id(
        blog_id=blog_id,
        db=db_session
    )


@router.put("/{blog_id}")
async def update_blog(
    blog_id: int,
    blog_data: BlogUpdateSerializer,
    db_session: AsyncSession = Depends(db.get_db),
    current_user: User = Depends(get_current_user)
):
    return await BlogController.update_blog(
        blog_id=blog_id,
        blog_data=blog_data,
        db=db_session,
        current_user=current_user
    )


@router.patch("/{blog_id}")
async def patch_blog(
    blog_id: int,
    blog_data: BlogPatchSerializer,
    db_session: AsyncSession = Depends(db.get_db),
    current_user=Depends(get_current_user)
):
    update_data = blog_data.model_dump(exclude_unset=True)

    return await BlogController.patch_blog(
        blog_id=blog_id,
        update_data=update_data,
        db=db_session,
        current_user=current_user
    )

@router.delete("/{blog_id}")
async def delete_blog(
    blog_id: int,
    db_session: AsyncSession = Depends(db.get_db),
    current_user: User = Depends(get_current_user)
):
    return await BlogController.delete_blog(
        blog_id=blog_id,
        db=db_session,
        current_user=current_user
    )