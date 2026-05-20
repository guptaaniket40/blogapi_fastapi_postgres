from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Blog


class BlogSchema:

    @classmethod
    async def get_blog_data(
        cls,
        db: AsyncSession,
        blog_id=None,
        user_id=None
    ):
        query = select(Blog)

        if blog_id:
            query = query.where(Blog.id == blog_id)

        if user_id:
            query = query.where(Blog.user_id == user_id)

        result = await db.execute(query)

        if blog_id:
            blog = result.scalar_one_or_none()
        else:
            blog = result.scalars().all()

        return blog

    @classmethod
    async def create_blog(
        cls,
        db: AsyncSession,
        request,
        image_url=None,
        user_id=None
    ):
        new_blog = Blog(
            title=request.title,
            content=request.content,
            author=request.author,
            image_url=image_url,
            user_id=user_id
        )

        db.add(new_blog)
        await db.commit()
        await db.refresh(new_blog)

        return new_blog

    @classmethod
    async def update_blog(
        cls,
        db: AsyncSession,
        blog,
        request,
        image_url=None
    ):
        blog.title = request.title
        blog.content = request.content
        blog.author = request.author

        if image_url:
            blog.image_url = image_url

        await db.commit()
        await db.refresh(blog)

        return blog

    @classmethod
    async def patch_blog(
        cls,
        db: AsyncSession,
        blog,
        update_data,
        image_url=None
    ):
        if "title" in update_data:
            blog.title = update_data["title"]

        if "content" in update_data:
            blog.content = update_data["content"]

        if "author" in update_data:
            blog.author = update_data["author"]

        if image_url:
            blog.image_url = image_url

        await db.commit()
        await db.refresh(blog)

        return blog

    @classmethod
    async def delete_blog(
        cls,
        db: AsyncSession,
        blog
    ):
        await db.delete(blog)
        await db.commit()

        return True