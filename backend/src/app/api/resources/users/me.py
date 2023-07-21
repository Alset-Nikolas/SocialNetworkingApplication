from fastapi import FastAPI, status, HTTPException, Depends
from app.services.user import UserService
from app.schemas.user import UserSchema
from fastapi import APIRouter, HTTPException, status, Depends
from app.orm.user import UserModel

router = APIRouter(prefix="")

@router.get('/me', summary='Get details of currently logged in user', response_model=UserSchema)
async def get_me(user: UserSchema = Depends(UserService.get_current_user)):
    return user