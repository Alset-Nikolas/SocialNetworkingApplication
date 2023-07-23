import typing as t
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.factory import get_session
from app.services.user import UserService
from app.schemas.user import UserSchema
from app.schemas.post import CreatePostSchema, GetPostSchema
from app.services.post import PostService
from fastapi import APIRouter, HTTPException, status, Depends
from app.orm.post import PostModel

router = APIRouter(prefix="/post/{post_id}")


@router.delete('', summary="Delete post", response_model=None)
async def delete_post(post_id: int, user: UserSchema = Depends(UserService.get_current_user),
                      db: Session = Depends(get_session)):
    post: PostModel = PostService(db, user).get(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"post id={post_id} not exist",
        )
    if not post.check_permission(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
        )
    
    PostService(db, user).delete(post)


@router.patch('', summary="Update post", response_model=None)
async def update_post(post_id: int, data: CreatePostSchema, user: UserSchema = Depends(UserService.get_current_user),
                      db: Session = Depends(get_session)):
    post: PostModel = PostService(db, user).get(post_id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"post id={post_id} not exist",
        )
    if not post.check_permission(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
        )
    PostService(db, user).update(post, data)
    
@router.get('', summary="Get post", response_model=GetPostSchema)
async def get_post(post_id: int, user: UserSchema = Depends(UserService.get_current_user),
                      db: Session = Depends(get_session)):
    post:t.Optional[PostModel] = PostService(db, user).get(post_id=post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post id={post_id} not exist'
        )
    return GetPostSchema(**post.to_json(user, db))