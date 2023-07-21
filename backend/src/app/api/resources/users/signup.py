import typing as t
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.user import LoginResponseSchema, UserSignUpSchema, UserSchema
from app.services.jwt import JwtService
from app.factory import get_session

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from fastapi import APIRouter, HTTPException, status, Depends
from app.services.user import UserOrmService, UserModel
router = APIRouter(prefix="")


@router.post('/signup', summary="Signup new user", response_model=LoginResponseSchema)
async def create_user(data: UserSignUpSchema, db: Session = Depends(get_session)):
    # querying database to check if user already exist
    user: UserModel = UserOrmService(db).create(data)
    if user is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    return LoginResponseSchema(user=UserSchema(**user.to_json()), tokens=JwtService.get_tokens(user.email))