from pydantic import BaseModel
from .jwt import TokenSchema

class UserSignUpSchema(BaseModel):
    email:str
    password:str


class UserSchema(BaseModel):
    id: int
    email:str

class LoginResponseSchema(BaseModel):
    user: UserSchema
    tokens: TokenSchema


