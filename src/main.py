from fastapi import FastAPI

from src.urls.v1.auth import router as auth_router
from src.urls.v1.blogs import router as blogs_router

app = FastAPI(
    title="Blog API",
    version="1.0.0"
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(blogs_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "Blog API is running"
    }