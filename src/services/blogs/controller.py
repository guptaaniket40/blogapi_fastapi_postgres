from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Blog, User
from src.services.blogs.schema import BlogCreate, BlogUpdate, BlogPatch
from src.services.blogs.serializers import serialize_blog, serialize_blog_list
from src.utils.response import success_response
from src.utils.s3_upload import (
    get_s3_key_from_url,
    upload_base64_image_to_s3,
    delete_image_from_s3
)


async def create_blog(
    blog_data: BlogCreate,
    db: AsyncSession,
    current_user: User
):
    image_url = None

    if blog_data.image_base64 and blog_data.image_name:
        image_url = await upload_base64_image_to_s3(
            blog_data.image_base64,
            blog_data.image_name
        )

    new_blog = Blog(
        title=blog_data.title,
        content=blog_data.content,
        author=blog_data.author,
        image_url=image_url,
        user_id=current_user.id
    )

    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)

    return success_response(
        "Blog created successfully",
        serialize_blog(new_blog)
    )


async def get_all_blogs(db: AsyncSession):
    result = await db.execute(select(Blog))
    blogs = result.scalars().all()

    return success_response(
        "Blogs fetched successfully",
        serialize_blog_list(blogs)
    )


async def get_blog_by_id(blog_id: int, db: AsyncSession):
    result = await db.execute(
        select(Blog).where(Blog.id == blog_id)
    )
    blog = result.scalar_one_or_none()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    return success_response(
        "Blog fetched successfully",
        serialize_blog(blog)
    )


async def update_blog(
    blog_id: int,
    blog_data: BlogUpdate,
    db: AsyncSession,
    current_user: User
):
    result = await db.execute(
        select(Blog).where(Blog.id == blog_id)
    )
    blog = result.scalar_one_or_none()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    if blog.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can update only your own blog"
        )

    blog.title = blog_data.title
    blog.content = blog_data.content
    blog.author = blog_data.author

    if blog_data.image_base64 and blog_data.image_name:
        if blog.image_url:
            old_file_key = get_s3_key_from_url(blog.image_url)
            await delete_image_from_s3(old_file_key)

        blog.image_url = await upload_base64_image_to_s3(
            blog_data.image_base64,
            blog_data.image_name
        )

    await db.commit()
    await db.refresh(blog)

    return success_response(
        "Blog updated successfully",
        serialize_blog(blog)
    )


async def patch_blog(
    blog_id: int,
    blog_data: BlogPatch,
    db: AsyncSession,
    current_user: User
):
    result = await db.execute(
        select(Blog).where(Blog.id == blog_id)
    )
    blog = result.scalar_one_or_none()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    if blog.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can update only your own blog"
        )

    update_data = blog_data.model_dump(exclude_unset=True)

    if "title" in update_data:
        blog.title = update_data["title"]

    if "content" in update_data:
        blog.content = update_data["content"]

    if "author" in update_data:
        blog.author = update_data["author"]

    if update_data.get("image_base64") and update_data.get("image_name"):
        if blog.image_url:
            old_file_key = get_s3_key_from_url(blog.image_url)
            await delete_image_from_s3(old_file_key)

        blog.image_url = await upload_base64_image_to_s3(
            update_data["image_base64"],
            update_data["image_name"]
        )

    await db.commit()
    await db.refresh(blog)

    return success_response(
        "Blog partially updated successfully",
        serialize_blog(blog)
    )


async def delete_blog(
    blog_id: int,
    db: AsyncSession,
    current_user: User
):
    result = await db.execute(
        select(Blog).where(Blog.id == blog_id)
    )
    blog = result.scalar_one_or_none()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    if blog.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can delete only your own blog"
        )

    if blog.image_url:
        await delete_image_from_s3(blog.image_url)

    await db.delete(blog)
    await db.commit()

    return success_response("Blog deleted successfully")