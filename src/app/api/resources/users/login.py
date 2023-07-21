import typing as t
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.jwt import TokenSchema
from app.services.password import PasswordService
from app.services.jwt import JwtService
from app.factory import get_session
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import APIRouter, HTTPException, status, Depends

router = APIRouter(prefix="")

db = {"admin":
{
        'email': "admin",
        'password': PasswordService.get_hashed_password("admin"),
        'id': 1
    }
}

@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.username )
    user = db.get(form_data.username, None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user['password']
    if not PasswordService.verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return JwtService.get_tokens(user['email']) 
