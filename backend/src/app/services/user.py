import typing as t
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.factory import SETTINGS, get_session

from jose import jwt
from pydantic import ValidationError
from app.schemas.jwt import TokenPayload
from app.schemas.user import UserSchema
from sqlalchemy.orm import Session
from app.orm import UserModel
from app.services.password import PasswordService

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/v1/users/login",
    scheme_name="JWT"
)

from app.schemas.user import LoginResponseSchema, UserSignUpSchema

class UserOrmService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email:str)->t.Optional[UserModel]:
        user: t.Optional[UserModel] = self.db \
            .query(UserModel) \
            .filter_by(email=email).first()
        return user
    
    def create(self, data:UserSignUpSchema)->t.Optional[UserModel]:
        if self.get_user_by_email(data.email) is None:
            data.password = PasswordService.get_hashed_password(data.password)
            new_user: UserModel = UserModel(**data.model_dump())
            self.db.add(new_user)
            self.db.commit()
            return new_user
        
        
class UserService:
    @staticmethod
    async def get_current_user(token: str = Depends(reuseable_oauth)) -> UserSchema:
        try:
            
            db: Session = next(get_session())
            
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
            
        user: t.Union[dict[str, t.Any], None] = UserOrmService(db).get_user_by_email(token_data.sub)
        
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )
        
        return UserSchema(**user.to_json())
    
   