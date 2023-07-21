import typing as t
from datetime import datetime, timedelta
from app.factory import SETTINGS
from jose import jwt
from app.schemas.jwt import TokenSchema, TokenPayload

class JwtService:
    @staticmethod
    def create_access_token(subject: t.Union[str, t.Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, SETTINGS.JWT_SECRET_KEY, SETTINGS.ALGORITHM)
        return encoded_jwt
    @staticmethod
    def create_refresh_token(subject: t.Union[str, t.Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=SETTINGS.REFRESH_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, SETTINGS.JWT_REFRESH_SECRET_KEY, SETTINGS.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def get_tokens(email:str)->TokenSchema:
        return TokenSchema(access_token=JwtService.create_access_token(email), refresh_token=JwtService.create_refresh_token(email))
     