from fastapi import APIRouter

from app.api.resources import test


api_router = APIRouter()

api_router.include_router(test.router, tags=["test"])
