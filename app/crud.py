from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from . import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()


# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Home route
@app.get("/")
def home():
    return {"msg": "Blog API running"}


# Get all blogs
@app.get("/blogs/")
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# Create blog
@app.post("/blogs/")
def create(blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    new_blog = models.Blog(**blog.dict())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# Get single blog
@app.get("/blogs/{id}")
def single_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Not found")

    return blog


# Update blog
@app.put("/blogs/{id}")
def update(id: int, blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    existing_blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not existing_blog:
        raise HTTPException(status_code=404, detail="Not found")

    existing_blog.title = blog.title
    existing_blog.content = blog.content
    existing_blog.author = blog.author

    db.commit()
    db.refresh(existing_blog)

    return existing_blog


# Delete blog
@app.delete("/blogs/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(blog)
    db.commit()

    return {"msg": "Deleted"}