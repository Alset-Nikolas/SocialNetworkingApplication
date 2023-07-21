from fastapi import APIRouter, HTTPException, status, Depends
from app.api.resources.posts import create
from app.api.resources.posts import fix_post
from app.api.resources.posts import list


posts_router = APIRouter(prefix='')

posts_router.include_router(create.router, tags=["posts"])
posts_router.include_router(fix_post.router, tags=["posts"])
posts_router.include_router(list.router, tags=["posts"])