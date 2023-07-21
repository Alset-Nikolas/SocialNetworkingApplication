import typing as t
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.factory import SETTINGS

from jose import jwt
from pydantic import ValidationError
from app.schemas.jwt import TokenPayload
from app.schemas.users import UserSchema

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/v1/users/login",
    scheme_name="JWT"
)


db = {
    "admin":{
    "id": 1,
    "email": "admin",
    "password": "admin",
    }
}

class UserService:
    async def get_current_user(token: str = Depends(reuseable_oauth)) -> UserSchema:
        try:
            payload = jwt.decode(
                token, SETTINGS.JWT_SECRET_KEY, algorithms=[SETTINGS.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
            
            if datetime.fromtimestamp(token_data.exp) < datetime.now():
                raise HTTPException(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except(jwt.JWTError, ValidationError) as err:
            print(err)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        user: t.Union[dict[str, t.Any], None] = db.get(token_data.sub, None)
        
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )
        
        return UserSchema(**user)