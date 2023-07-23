from pydantic import BaseModel
from .jwt import TokenSchema


class UserSignUpSchema(BaseModel):
    email: str
    username: str
    password: str


class UserSchema(BaseModel):
    id: int
    username: str
    email: str


class LoginResponseSchema(BaseModel):
    access_token: str
    token_type: str
    token_expiry: str