import typing as t
from sqlalchemy.orm import Session
from app.orm.post import PostModel
from app.orm.user import UserModel
from app.schemas.post import GetPostSchema
from app.schemas.post import CreatePostSchema
from fastapi import APIRouter, HTTPException, status

class PostService:
    def __init__(self, db: Session, user: t.Optional[UserModel]):
        self.db = db
        self.user = user

    def create(self, text: str) -> t.Optional[PostModel]:
        post: PostModel = PostModel(text=text, author_id=self.user.id)
        self.db.add(post)
        self.db.commit()
        return GetPostSchema(**post.to_json(user=self.user, db=self.db))

    def get(self, post_id: int) -> t.Optional[PostModel]:
        post: t.Optional[PostModel] = self.db \
            .query(PostModel) \
            .get(post_id)
        return post

    def delete(self, post: PostModel) -> None:
        self.db.delete(post)
        self.db.commit()

    def update(self, post: PostModel, post_update: CreatePostSchema) -> None:
        if post_update.text:
            post.text = post_update.text

        self.db.commit()

    def get_all(self) -> t.List[GetPostSchema]:
        posts: t.List[PostModel] = self.db \
            .query(PostModel) \
            .all()
        return [GetPostSchema(**p.to_json(user=self.user, db=self.db)) for p in posts]
