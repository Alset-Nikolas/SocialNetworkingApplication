import typing as t
from sqlalchemy.orm import Session
from app.orm.post import PostModel
from app.orm.user import UserModel
from app.schemas.post import GetPostSchema
from app.schemas.post import CreatePostSchema

class PostService:
    def __init__(self, db: Session, user:t.Optional[UserModel]):
        self.db = db
        self.user = user

    def create(self, text:str)->t.Optional[PostModel]:
        post: PostModel = PostModel(text=text, author_id=self.user.id)
        self.db.add(post)
        self.db.commit()        
        return GetPostSchema(**post.to_json(user=self.user, db=self.db))
    
    def get(self, post_id:int) ->t.Optional[PostModel]:
        post: t.Optional[PostModel] = self.db \
            .query(PostModel) \
            .get(post_id)
        return post

    def delete(self, post_id:int) ->t.Tuple[bool, str]:
        post:t.Optional[PostModel] = self.get(post_id)
        if post is None:
            return False, f"Post id={post_id} not exist"
        if not post.check_permission(self.user):
            return False, f"Permission denied"
        self.db.delete(post)
        self.db.commit()
        return True, None
    
    def update(self, post_id:int, post_update:CreatePostSchema)->t.Tuple[bool, str]:
        post:t.Optional[PostModel] = self.get(post_id)
        if post is None:
            return False, f"Post id={post_id} not exist"
        if not post.check_permission(self.user):
            return False, f"Permission denied"
        if post_update.text:
            post.text = post_update.text

        self.db.commit()
        return True, None

    def get_all(self) -> t.List[GetPostSchema]:
        posts:t.List[PostModel] =  self.db \
            .query(PostModel) \
            .all()
        return [GetPostSchema(**p.to_json(user=self.user, db=self.db)) for p in posts]
