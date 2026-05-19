import base64
import uuid
from urllib.parse import urlparse

import aioboto3
from fastapi import HTTPException, status

from src.database.config import settings


def get_s3_image_url(file_key: str) -> str:
    return (
        f"https://{settings.AWS_BUCKET_NAME}.s3."
        f"{settings.AWS_REGION}.amazonaws.com/{file_key}"
    )


def get_s3_key_from_url(image_url: str) -> str:
    parsed_url = urlparse(image_url)
    return parsed_url.path.lstrip("/")


async def upload_base64_image_to_s3(image_base64: str, image_name: str) -> str:
    try:
        if "," in image_base64:
            image_base64 = image_base64.split(",")[1]

        image_bytes = base64.b64decode(image_base64)

        file_extension = image_name.split(".")[-1].lower()
        safe_image_name = image_name.replace(" ", "-")

        file_key = f"blogs/{uuid.uuid4()}-{safe_image_name}"

        content_type = f"image/{file_extension}"

        if file_extension in ["jpg", "jpeg"]:
            content_type = "image/jpeg"
        elif file_extension == "png":
            content_type = "image/png"
        elif file_extension == "webp":
            content_type = "image/webp"

        session = aioboto3.Session()

        async with session.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        ) as s3_client:
            await s3_client.put_object(
                Bucket=settings.AWS_BUCKET_NAME,
                Key=file_key,
                Body=image_bytes,
                ContentType=content_type,
            )

        return get_s3_image_url(file_key)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image upload failed: {str(e)}"
        )


async def delete_image_from_s3(image_url: str) -> None:
    try:
        image_key = get_s3_key_from_url(image_url)

        session = aioboto3.Session()

        async with session.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        ) as s3_client:
            await s3_client.delete_object(
                Bucket=settings.AWS_BUCKET_NAME,
                Key=image_key,
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image delete failed: {str(e)}"
        )