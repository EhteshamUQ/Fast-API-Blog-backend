from typing import Optional

from pydantic import BaseModel


class CreateBlogDTO(BaseModel):
    title: str
    content: str
    tags: str
    author_id: Optional[str] = None


class BlogDTO(CreateBlogDTO):
    id: str
    author_id: str


class EditBlogDTO(CreateBlogDTO):
    id: str
