from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

from sqlmodel import Field, Relationship, SQLModel

from utils.security import encrypt_password, validate_password


class RoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(SQLModel, table=True):
    id: str = Field(default=uuid4().hex, primary_key=True)
    name: str
    email: str = Field(unique=True)
    password: bytes
    date_of_birth: Optional[datetime]
    role: RoleEnum
    blogs: Optional["Blog"] = Relationship(back_populates="author")  # noqa: F821

    def __init__(
        self,
        name: str,
        password: str,
        email: str,
        date_of_birth: Optional[datetime],
        role: RoleEnum,
    ):
        self.name = name
        self.password = encrypt_password(password)
        self.email = email
        self.date_of_birth = date_of_birth
        self.role = role

    def validate_user_password(self, plain_password: str) -> bool:
        return validate_password(plain_password=plain_password, hashed_pw=self.password)
