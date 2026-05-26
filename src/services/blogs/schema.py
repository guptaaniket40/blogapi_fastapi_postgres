from sqlalchemy import select

from src.database.models import Blog
from src.database.db_config import db


 

class BlogSchema:

    @classmethod
    async def get_all_blogs(
        cls,
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
            return result.scalar_one_or_none()

        return result.scalars().all()
    
    @classmethod
    async def create_blog(
        cls,
        request,
        image_url,
        user_id
    ):
        blog = Blog(
            title=request.title,
            content=request.content,
            author=request.author,
            image_url=image_url,
            user_id=user_id
        )

        db.add(blog)
        await db.commit()
        await db.refresh(blog)

        return blog

    @classmethod
    async def update_blog(
        cls,
        blog,
        request,
        image_url=None
    ):
        blog.title = request.title
        blog.content = request.content
        blog.author = request.author

        if image_url is not None:
            blog.image_url = image_url

        await db.commit()
        await db.refresh(blog)

        return blog

    @classmethod
    async def patch_blog(
        cls,
        blog,
        update_data,
        image_url=None
    ):
        for key, value in update_data.items():
            if value is not None and hasattr(blog, key):
                setattr(blog, key, value)

        if image_url is not None:
            blog.image_url = image_url

        await db.commit()
        await db.refresh(blog)

        return blog

    @classmethod
    async def delete_blog(
        cls,
        blog
    ):
        await db.delete(blog)
        await db.commit()

        return True