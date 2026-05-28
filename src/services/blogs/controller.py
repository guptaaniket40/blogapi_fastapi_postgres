from fastapi import HTTPException, status

from src.services.blogs.schema import BlogSchema
from src.services.blogs.serializers import BlogResponseSerializer
from src.utils.s3_upload import (
    upload_base64_image_to_s3,
    delete_image_from_s3
)
from src.utils.response import success_response


class BlogController:

    @classmethod
    async def get_all_blogs(cls):
        blogs = await BlogSchema.get_all_blogs()

        blog_data = [
            BlogResponseSerializer.model_validate(blog).model_dump(mode="json")
            for blog in blogs
        ]

        return success_response(
            message="Blogs fetched successfully",
            data=blog_data
        )

    @classmethod
    async def get_blog_by_id(
        cls,
        blog_id
    ):
        blog = await BlogSchema.get_all_blogs(
            blog_id=blog_id
        )

        if not blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog not found"
            )

        blog_data = BlogResponseSerializer.model_validate(blog).model_dump(mode="json")

        return success_response(
            message="Blog fetched successfully",
            data=blog_data
        )

    @classmethod
    async def create_blog(
        cls,
        blog_data,
        current_user
    ):
        image_url = None

        if blog_data.image_base64 and blog_data.image_name:
            image_url = await upload_base64_image_to_s3(
                image_base64=blog_data.image_base64,
                image_name=blog_data.image_name
            )

        blog = await BlogSchema.create_blog(
            request=blog_data,
            image_url=image_url,
            user_id=current_user.id
        )

        blog_response = BlogResponseSerializer.model_validate(blog).model_dump(mode="json")

        return success_response(
            message="Blog created successfully",
            data=blog_response
        )

    @classmethod
    async def update_blog(
        cls,
        blog_id,
        blog_data,
        current_user
    ):
        blog = await BlogSchema.get_all_blogs(
            blog_id=blog_id
        )

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

        image_url = None

        if blog_data.image_base64 and blog_data.image_name:
            if blog.image_url:
                await delete_image_from_s3(
                    image_url=blog.image_url
                )

            image_url = await upload_base64_image_to_s3(
                image_base64=blog_data.image_base64,
                image_name=blog_data.image_name
            )

        updated_blog = await BlogSchema.update_blog(
            blog=blog,
            request=blog_data,
            image_url=image_url
        )

        blog_response = BlogResponseSerializer.model_validate(updated_blog).model_dump(mode="json")

        return success_response(
            message="Blog updated successfully",
            data=blog_response
        )

    @classmethod
    async def patch_blog(
        cls,
        blog_id,
        update_data,
        current_user
    ):
        blog = await BlogSchema.get_all_blogs(
            blog_id=blog_id
        )

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

        image_url = None

        if update_data.get("image_base64") and update_data.get("image_name"):
            if blog.image_url:
                await delete_image_from_s3(
                    image_url=blog.image_url
                )

            image_url = await upload_base64_image_to_s3(
                image_base64=update_data.get("image_base64"),
                image_name=update_data.get("image_name")
            )

        updated_blog = await BlogSchema.patch_blog(
            blog=blog,
            update_data=update_data,
            image_url=image_url
        )

        blog_response = BlogResponseSerializer.model_validate(updated_blog).model_dump(mode="json")

        return success_response(
            message="Blog partially updated successfully",
            data=blog_response
        )

    @classmethod
    async def delete_blog(
        cls,
        blog_id,
        current_user
    ):
        blog = await BlogSchema.get_all_blogs(
            blog_id=blog_id
        )

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
            await delete_image_from_s3(
                image_url=blog.image_url
            )

        await BlogSchema.delete_blog(
            blog=blog
        )

        return success_response(
            message="Blog deleted successfully",
            data=None
        )