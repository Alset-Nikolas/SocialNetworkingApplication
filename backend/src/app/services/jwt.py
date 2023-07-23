import typing as t
from datetime import datetime, timedelta
from app.factory import SETTINGS
from jose import jwt
from app.schemas.jwt import TokenSchema, TokenPayload, TokenExpirySchema
from pydantic import ValidationError


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
    def decode_access_token(token: str) -> t.Tuple[str, t.Optional[str]]:
        try:
            payload = jwt.decode(
                token, SETTINGS.JWT_SECRET_KEY, algorithms=[SETTINGS.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
            if datetime.fromtimestamp(token_data.exp) < datetime.now():
                return "", 'access token expiry'
        except(jwt.JWTError, ValidationError) as err:
            print(err)
            return "", err
        return token_data.sub, None
    
    @staticmethod
    def decode_refresh_token(token: str) -> t.Tuple[str, t.Optional[str]]:
        try:
            payload = jwt.decode(
                token, SETTINGS.JWT_REFRESH_SECRET_KEY, algorithms=[SETTINGS.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
            if datetime.fromtimestamp(token_data.exp) < datetime.now():
                return "", 'access token expiry'
        except(jwt.JWTError, ValidationError, AttributeError) as err:
            print(err)
            return "", 'jwt not valid refresh_token'
        return token_data.sub, None

    @staticmethod
    def get_tokens_expiry() -> TokenExpirySchema:
        return TokenExpirySchema(access_token_expiry=datetime.utcnow() + timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES),
                                 refresh_token_expiry=datetime.utcnow() + timedelta(minutes=SETTINGS.REFRESH_TOKEN_EXPIRE_MINUTES))

    @staticmethod
    def get_tokens(email: str, expires_delta:t.Optional[int]=None) -> TokenSchema:
        return TokenSchema(access_token=JwtService.create_access_token(email, expires_delta),
                           refresh_token=JwtService.create_refresh_token(email, expires_delta))
