from fastapi import APIRouter, HTTPException, status, Depends
from app.api.resources.grade_post import grade



grade_router = APIRouter(prefix='')

grade_router.include_router(grade.router, tags=["grade"])