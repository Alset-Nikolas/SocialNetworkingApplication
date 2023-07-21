import base64
import typing as t
from datetime import datetime

from sqlalchemy import (Column, Integer, String, Boolean, ARRAY, Float,
                        DateTime, ForeignKey)

from app.factory import BASE 
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from .grade_post import GradeModel

class PostModel(BASE):
    __tablename__ = 'post_table'

    id: Mapped[int] = Column(Integer, primary_key=True)
    author_id : Mapped[int]= mapped_column(ForeignKey('user_table.id'))
    author: Mapped["UserModel"] = relationship(back_populates="posts")

    date = Column(DateTime, default=datetime.now)
    text = Column(String)

    def to_json(self, user=None, db=None):
        is_like = False
        if db:
            grade = db.query(GradeModel).filter_by(post_id=self.id, user_id=user.id).first()
            if grade:
                is_like = grade.like

        return dict(
            id=self.id,
            author_id=self.author_id,
                    author_email=self.author.email,
                    text=self.text, date=self.date,
                    is_author=self.check_permission(user),
                    is_like=is_like)
    
    def check_permission(self, user) -> bool:
        if hasattr(user, 'id'):
            return self.author_id == user.id
        return False
        
