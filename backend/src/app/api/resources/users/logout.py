from app.services.user import UserService
from app.schemas.user import UserSchema
from app.orm.user import UserModel
from fastapi.responses import JSONResponse
from fastapi import APIRouter, HTTPException, status, Depends, Cookie

router = APIRouter(prefix="")


@router.get('/logout', summary='Logout user')
async def logout(refresh_token: str = Cookie(None, description="Refresh token id")):
    response = JSONResponse(
        content= {'status': 'success'}
    )
    response.delete_cookie('refresh_token')
    return response
