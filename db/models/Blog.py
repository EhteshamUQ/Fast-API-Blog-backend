from uuid import uuid4

from sqlmodel import Field, Relationship, SQLModel


class Blog(SQLModel, table=True):
    id: str = Field(default=uuid4().hex, primary_key=True)
    content: str
    title: str
    tags: str
    author_id: str = Field(foreign_key="user.id")
    author: "User" = Relationship(back_populates="blogs")  # noqa: F821
    is_deleted: bool = Field(default=False)
