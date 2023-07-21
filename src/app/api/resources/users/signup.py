import typing as t
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.users import LoginResponseSchema, UserSignUpSchema
from app.services.password import PasswordService
from app.services.jwt import JwtService
from app.factory import get_session

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from fastapi import APIRouter, HTTPException, status, Depends

router = APIRouter(prefix="")

db = dict()

@router.post('/signup', summary="Signup new user", response_model=LoginResponseSchema)
async def create_user(data: UserSignUpSchema):
    # querying database to check if user already exist
    user = db.get(data.email, None)
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = {
        'email': data.email,
        'password': PasswordService.get_hashed_password(data.password),
        'id': 1
    }
    db[data.email] = user  
    return LoginResponseSchema(user=user, tokens=JwtService.get_tokens(user['email']))