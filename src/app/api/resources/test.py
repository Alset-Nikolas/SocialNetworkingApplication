import typing as t
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.test import TestSchema
from app import get_session

router = APIRouter(prefix="/test")


@router.get("", response_model=TestSchema)
def get_picture_for_challenge_handler(db: Session = Depends(get_session), picture_id: t.Optional[int]=None):
    """
    Get picture for challenge
    """

    return {"id": 1}
