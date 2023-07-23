import typing as t
from pydantic import BaseModel
from datetime import datetime


class GradePostSchema(BaseModel):
    like: bool
