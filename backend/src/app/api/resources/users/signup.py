import typing as t
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.user import LoginResponseSchema, UserSignUpSchema, UserSchema
from app.services.jwt import JwtService
from app.factory import get_session, SETTINGS

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from app.services.user import UserOrmService, UserModel
from fastapi import APIRouter, HTTPException, status, Depends, Response

router = APIRouter(prefix="")

@router.post('/signup', summary="Signup new user", response_model=UserSchema)
async def create_user(response: Response, data: UserSignUpSchema, db: Session = Depends(get_session)):
    # querying database to check if user already exist
    user: UserModel = UserOrmService(db).create(data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    return UserSchema(**user.to_json())
