import typing as t
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.factory import get_session
from app.services.user import UserService
from app.schemas.user import UserSchema
from app.schemas.post import GetPostSchema, CreatePostSchema
from app.schemas.grade import GradePostSchema

from app.services.post import PostService, PostModel
from app.services.grade import GradeService

from fastapi import APIRouter, HTTPException, status, Depends

router = APIRouter(prefix="/grade/{post_id}")



@router.post('', summary="Grade post", response_model=GetPostSchema)
async def grade_post(post_id:int, data: GradePostSchema, user: UserSchema = Depends(UserService.get_current_user), db: Session = Depends(get_session)):
    post:PostModel = PostService(db,user ).get(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"post id={post_id} not exist",
        )
    if post.check_permission(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Author not like/dislike",
        )
    GradeService(db, user).update(post=post, like=data.like)
    return GetPostSchema(**post.to_json(user=user, db=db))


@router.delete('', summary="Delete Grade post", response_model=GetPostSchema)
async def delete_grade_post(post_id:int, user: UserSchema = Depends(UserService.get_current_user), db: Session = Depends(get_session)):
    post:PostModel = PostService(db,user ).get(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"post id={post_id} not exist",
        )
    if post.check_permission(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Author not like/dislike",
        )
    post:GetPostSchema = GradeService(db, user).delete(post=post, like=GradePostSchema.like)
    return post