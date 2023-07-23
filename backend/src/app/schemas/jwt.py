import typing as t
from pydantic import BaseModel
from datetime import datetime


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenExpirySchema(BaseModel):
    access_token_expiry: datetime
    refresh_token_expiry: datetime

class TokenPayload(BaseModel):
    sub: t.Union[str, t.Any]
    exp: int
