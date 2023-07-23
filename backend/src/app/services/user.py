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
from app.factory import get_session, SETTINGS
from .jwt import JwtService


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/v1/users/login",
    scheme_name="JWT"
)

from app.schemas.user import LoginResponseSchema, UserSignUpSchema


class UserOrmService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> t.Optional[UserModel]:
        user: t.Optional[UserModel] = self.db \
            .query(UserModel) \
            .filter_by(email=email).first()
        return user
    
    def get_user_by_username(self, username: str) -> t.Optional[UserModel]:
        user: t.Optional[UserModel] = self.db \
            .query(UserModel) \
            .filter_by(username=username).first()
        return user
    
    def get_all(self) -> t.List[UserModel]:
        return self.db.query(UserModel).all()

    def create(self, data: UserSignUpSchema) -> t.Optional[UserModel]:
        if self.get_user_by_email(data.email) is None and self.get_user_by_username(data.username) is None:
            data.password = PasswordService.get_hashed_password(data.password)
            new_user: UserModel = UserModel(**data.model_dump())
            self.db.add(new_user)
            self.db.commit()
            return new_user


class UserService:
    @staticmethod
    async def get_current_user(token: str = Depends(reuseable_oauth), db: Session = Depends(get_session),) -> UserSchema:
        user_email, err = JwtService.decode_access_token(token)
        if err:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(err),
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user: t.Union[dict[str, t.Any], None] = UserOrmService(db).get_user_by_email(user_email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )

        return UserSchema(**user.to_json())

    