from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.models.Blog import Blog

from db.models.User import User, RoleEnum
from db.repository.blog import (
    archive_blog_in_db,
    get_all_blogs,
    create_blog as create_blog,
    get_blog_by_id,
    update_blog,
)
from db.repository.user import get_current_user
from db.session import get_db_session
from models.blog import BlogDTO, CreateBlogDTO, EditBlogDTO

blog_router = APIRouter(prefix="/blogs", tags=["Blogs"])


@blog_router.get("/", response_model=List[BlogDTO])
def get_blogs(
    session: Session = Depends(get_db_session), user: User = Depends(get_current_user)
):
    return get_all_blogs(session)


@blog_router.post("/", response_model=BlogDTO)
def create_blog_path(
    blog_details: CreateBlogDTO,
    session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    blog_details.author_id = user.id
    return create_blog(blog_details=blog_details, session=session)


@blog_router.patch("/", response_model=BlogDTO)
def update_a_blog(
    blog_details: EditBlogDTO,
    session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    blog: Blog = get_blog_by_id(blog_details.id)
    if user.id != blog.author_id and user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=409,
            detail="Cannot update as the current user is not the author of this blog",
        )
    updated_blog = update_blog(blog, blog_details, session)
    return updated_blog


@blog_router.delete("/{blog_id}", response_model=bool)
def archive_blog(
    blog_id: str,
    session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
):
    blog: Blog = get_blog_by_id(blog_id)
    if user.id != blog.author_id and user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=409,
            detail="Cannot update as the current user is not the author of this blog",
        )
    blog = archive_blog_in_db(blog, session)
    if blog.is_deleted is False:
        return True
    return False
