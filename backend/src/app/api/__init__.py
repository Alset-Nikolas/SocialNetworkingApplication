from fastapi import APIRouter

from app.api.resources.users import users_router
from app.api.resources.posts import posts_router
from app.api.resources.grade_post import grade_router
from app.orm import *

api_router = APIRouter()

api_router.include_router(users_router, tags=["users"])
api_router.include_router(posts_router, tags=["posts"])
api_router.include_router(grade_router, tags=["grade"])
