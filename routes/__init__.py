from fastapi import APIRouter

from .v1.blog import blog_router
from .v1.login import login_router
from .v1.user import user_router

base_router = APIRouter(prefix="/v1")

base_router.include_router(user_router)
base_router.include_router(login_router)
base_router.include_router(blog_router)
