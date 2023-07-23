import typing as t
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.factory import get_session
from app.services.user import UserService
from app.schemas.user import UserSchema
from app.schemas.post import GetPostSchema, CreatePostSchema
from app.services.post import PostService

router = APIRouter(prefix="/posts")


@router.get('', summary="Get list post", response_model=t.List[GetPostSchema])
async def get_list_post(db: Session = Depends(get_session), user: UserSchema = Depends(UserService.get_current_user)):
    return PostService(db, user).get_all()
