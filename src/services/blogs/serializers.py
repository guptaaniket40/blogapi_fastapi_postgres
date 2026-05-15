def serialize_blog(blog):
    return {
        "id": blog.id,
        "title": blog.title,
        "content": blog.content,
        "author": blog.author,
        "user_id": blog.user_id,
        "created_at": blog.created_at.isoformat() if blog.created_at else None
    }


def serialize_blog_list(blogs):
    return [serialize_blog(blog) for blog in blogs]