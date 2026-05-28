from fastapi import APIRouter, Depends

from src.services.blogs.controller import BlogController
from src.services.blogs.serializers import (
    BlogCreateSerializer,
    BlogUpdateSerializer,
    BlogPatchSerializer
)

from src.utils.security import get_current_user


router = APIRouter(prefix="/blogs",tags=["Blogs"])


@router.get("/")
async def get_all_blogs():
    return await BlogController.get_all_blogs()


@router.get("/{blog_id}")
async def get_blog_by_id(
    blog_id: int
):
    return await BlogController.get_blog_by_id(
        blog_id=blog_id
    )


@router.post("/")
async def create_blog(
    request: BlogCreateSerializer,
    current_user=Depends(get_current_user)
):
    return await BlogController.create_blog(
        blog_data=request,
        current_user=current_user
    )


@router.put("/{blog_id}")
async def update_blog(
    blog_id: int,
    request: BlogUpdateSerializer,
    current_user=Depends(get_current_user)
):
    return await BlogController.update_blog(
        blog_id=blog_id,
        blog_data=request,
        current_user=current_user
    )


@router.patch("/{blog_id}")
async def patch_blog(
    blog_id: int,
    request: BlogPatchSerializer,
    current_user=Depends(get_current_user)
):
    update_data = request.model_dump(exclude_unset=True)

    return await BlogController.patch_blog(
        blog_id=blog_id,
        update_data=update_data,
        current_user=current_user
    )


@router.delete("/{blog_id}")
async def delete_blog(
    blog_id: int,
    current_user=Depends(get_current_user)
):
    return await BlogController.delete_blog(
        blog_id=blog_id,
        current_user=current_user
    )