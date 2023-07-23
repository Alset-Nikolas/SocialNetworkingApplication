import typing as t
from pydantic import BaseModel
from datetime import datetime


class CreatePostSchema(BaseModel):
    text: str


class GetPostSchema(BaseModel):
    id: int
    text: str
    date: datetime
    author_email: str
    is_author: bool
    is_like: t.Optional[bool] = None
