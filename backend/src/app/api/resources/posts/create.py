import typing as t
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.factory import get_session
from app.services.user import UserService
from app.schemas.user import UserSchema
from app.schemas.post import GetPostSchema, CreatePostSchema
from app.services.post import PostService

router = APIRouter(prefix="/post")


@router.post('', summary="Create post", response_model=GetPostSchema)
async def create_post(data: CreatePostSchema, user: UserSchema = Depends(UserService.get_current_user),
                      db: Session = Depends(get_session)):
    post: GetPostSchema = PostService(db, user).create(text=data.text)
    return post
