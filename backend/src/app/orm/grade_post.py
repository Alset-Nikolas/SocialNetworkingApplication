import base64
import typing as t
from datetime import datetime

from sqlalchemy import (Column, Integer, String, Boolean, ARRAY, Float,
                        DateTime, ForeignKey)

from app.factory import BASE
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped


class GradeModel(BASE):
    __tablename__ = 'grade_table'

    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_table.id'))
    user: Mapped["UserModel"] = relationship()
    post_id: Mapped[int] = mapped_column(ForeignKey('post_table.id'))
    post: Mapped["PostModel"] = relationship()
    like: bool = Column(Boolean, nullable=False)

    def to_json(self, user=None):
        print(user)
        return dict(author_id=self.author_id,
                    author_email=self.author.email,
                    text=self.text, date=self.date,
                    is_author=self.check_permission(user))

    def check_permission(self, user) -> bool:
        print(self.author_id, user)
        if hasattr(user, 'id'):
            return self.author_id == user.id
        return False
