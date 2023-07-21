import typing as t
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.jwt import TokenSchema
from app.services.password import PasswordService
from app.services.jwt import JwtService
from app.factory import get_session
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import APIRouter, HTTPException, status, Depends
from app.services.user import UserOrmService, UserModel

router = APIRouter(prefix="")



@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user: UserModel = UserOrmService(db).get_user_by_email(form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    if not PasswordService.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return JwtService.get_tokens(user.email) 
