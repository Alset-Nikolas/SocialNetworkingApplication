import typing as t
from sqlalchemy.orm import Session
from app.orm.post import PostModel
from app.orm.user import UserModel
from app.orm.grade_post import GradeModel

from app.schemas.post import GetPostSchema
from app.schemas.post import CreatePostSchema


class GradeService:
    def __init__(self, db: Session, user: t.Optional[UserModel]):
        self.db = db
        self.user = user

    def update(self, post: PostModel, like: bool):
        grade = self.get(post)
        if not grade:
            grade = GradeModel(post_id=post.id, user_id=self.user.id, like=like)
        grade.like = like
        self.db.add(grade)
        self.db.commit()

    def get(self, post: PostModel):
        return self.db.query(GradeModel).filter_by(post_id=post.id, user_id=self.user.id).first()

    def delete(self, post: PostModel) -> bool:
        grade = self.get(post)
        if grade is not None:
            self.db.delete(grade)
            self.db.commit()
            return True
        return False
