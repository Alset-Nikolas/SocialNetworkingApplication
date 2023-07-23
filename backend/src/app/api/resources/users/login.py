import typing as t
from fastapi import APIRouter, HTTPException, status, Depends, Cookie
from sqlalchemy.orm import Session
from app.schemas.jwt import TokenSchema
from app.schemas.user import LoginResponseSchema
from app.services.password import PasswordService
from app.services.jwt import JwtService
from app.factory import get_session, SETTINGS
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import APIRouter, HTTPException, status, Depends, Response
from app.services.user import UserOrmService, UserModel
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse


router = APIRouter(prefix="")


@router.post('/login', summary="Create access and refresh tokens for user", response_model=LoginResponseSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user: UserModel = UserOrmService(db).get_user_by_username(form_data.username)
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
    tokens = JwtService.get_tokens(user.email)
    tokens_times_expiry = JwtService.get_tokens_expiry()

    
    response = JSONResponse(
        content={
            "access_token": tokens.access_token,
            "token_type": "Bearer",
            "token_expiry": str(tokens_times_expiry.access_token_expiry),
        }
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        expires=str(tokens_times_expiry.refresh_token_expiry),
        httponly=True,
    )


    return response
