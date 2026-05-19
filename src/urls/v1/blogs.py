from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_config import get_db
from src.database.models import User
from src.services.blogs.schema import BlogCreate, BlogUpdate
from src.services.blogs import controller
from src.utils.security import get_current_user

router = APIRouter(prefix="/blogs", tags=["Blogs"])


@router.post("/")
async def create_blog(
    blog_data: BlogCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await controller.create_blog(blog_data, db, current_user)


@router.get("/")
async def get_all_blogs(
    db: AsyncSession = Depends(get_db)
):
    return await controller.get_all_blogs(db)


@router.get("/{blog_id}")
async def get_blog_by_id(
    blog_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await controller.get_blog_by_id(blog_id, db)


@router.put("/{blog_id}")
async def update_blog(
    blog_id: int,
    blog_data: BlogUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await controller.update_blog(blog_id, blog_data, db, current_user)


@router.delete("/{blog_id}")
async def delete_blog(
    blog_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await controller.delete_blog(blog_id, db, current_user)