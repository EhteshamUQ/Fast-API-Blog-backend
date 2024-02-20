from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from db.models.User import RoleEnum


class UserData(BaseModel):
    name: str
    email: EmailStr
    password: str
    date_of_birth: Optional[datetime]
    role: RoleEnum


class UserResponse(BaseModel):
    name: str
    email: EmailStr
    date_of_birth: Optional[datetime]
    id: str
    role: RoleEnum


class UserUpdateData(BaseModel):
    name: str
    id: str
    date_of_birth: Optional[datetime]
