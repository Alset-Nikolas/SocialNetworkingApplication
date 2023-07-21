import typing as t
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.factory import get_session
from app.services.user import UserService
from app.schemas.user import UserSchema
from app.schemas.post import CreatePostSchema
from app.services.post import PostService
from fastapi import APIRouter, HTTPException, status, Depends

router = APIRouter(prefix="/post/{post_id}")


@router.delete('', summary="Delete post", response_model=None)
async def delete_post(post_id: int, user: UserSchema = Depends(UserService.get_current_user), db: Session = Depends(get_session)):
    result, err_text = PostService(db, user).delete(post_id=post_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=err_text
        )

@router.patch('', summary="Update post", response_model=None)
async def update_post(post_id: int, data: CreatePostSchema, user: UserSchema = Depends(UserService.get_current_user), db: Session = Depends(get_session)):
    result, err_text = PostService(db, user).update(post_id=post_id, post_update=data)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=err_text
        )
