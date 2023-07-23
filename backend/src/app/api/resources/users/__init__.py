from fastapi import APIRouter, HTTPException, status, Depends
from app.api.resources.users import signup
from app.api.resources.users import login
from app.api.resources.users import me
from app.api.resources.users import refresh

users_router = APIRouter(prefix='/users')

users_router.include_router(signup.router, tags=["users"])
users_router.include_router(login.router, tags=["users"])
users_router.include_router(me.router, tags=["users"])
users_router.include_router(refresh.router, tags=["users"])