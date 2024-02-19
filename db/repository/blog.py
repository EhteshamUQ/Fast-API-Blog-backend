from fastapi import HTTPException
from sqlmodel import Session, select

from db.models.Blog import Blog
from models.blog import CreateBlogDTO, EditBlogDTO


def get_all_blogs(session: Session):
    try:
        query = select(Blog).where(Blog.is_deleted == False)  # noqa: E712
        result = session.exec(query).all()
        return result
    except Exception:
        raise HTTPException(
            status_code=500, detail="There was an error while fetching blogs"
        )


def create_blog(blog_details: CreateBlogDTO, session: Session) -> Blog:
    try:
        blog = Blog(
            author_id=blog_details.author_id,
            content=blog_details.content,
            title=blog_details.title,
            tags=blog_details.tags,
        )
        session.add(blog)
        session.commit()
        return blog
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=500, detail="There was an error while creating blog"
        )


def update_blog(blog: Blog, updated_values: EditBlogDTO, session: Session) -> Blog:
    try:
        blog.title = updated_values.title
        blog.content = updated_values.content
        blog.tags = updated_values.tags
        session.commit()
        return blog
    except Exception as e:
        print(e)
        session.rollback()
        raise HTTPException(status_code=500, detail="Error occured while updating blog")


def get_blog_by_id(blog_id: str, session: Session) -> Blog:
    try:
        statement = select(Blog).where(Blog.id == blog_id)
        blog = session.exec(statement=statement).one()
        return blog
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error occured")


def archive_blog_in_db(blog: Blog, session: Session):
    try:
        blog.is_deleted = True
        session.commit()
        return blog
    except Exception as e:
        print(e)
        session.rollback()
        raise HTTPException(
            status_code=500, detail="Error occured while archiving blog"
        )
