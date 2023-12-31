import base64
import typing as t
from datetime import datetime
from sqlalchemy.orm import relationship

from sqlalchemy import (Column, Integer, String, Boolean, ARRAY, Float,
                        DateTime, ForeignKey, )

from app.factory import BASE
from sqlalchemy.orm import Mapped


class UserModel(BASE):
    __tablename__ = 'user_table'

    id: Mapped[int] = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String)
    posts: Mapped["PostModel"] = relationship(back_populates="author", cascade="all,delete",)

    def to_json(self):
        return dict(id=self.id,
                    email=self.email,
                    username=self.username)


# alembic revision --autogenerate -m 'add username'
# alembic upgrade head