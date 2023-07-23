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


@router.get('/refresh', summary="Refresh access token", response_model=LoginResponseSchema)
async def login(db: Session = Depends(get_session), refresh_token: str = Cookie(None, description="Refresh token id")):
    email_user, err = JwtService.decode_refresh_token(refresh_token)
    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )
    user: UserModel = UserOrmService(db).get_user_by_email(email_user)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email"
        )
    access_token_expires = timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JwtService.create_access_token(subject=email_user, expires_delta=access_token_expires)
    return LoginResponseSchema(
        access_token= access_token,
        token_type='Bearer',
        token_expiry=str(datetime.utcnow() + access_token_expires),
    )  