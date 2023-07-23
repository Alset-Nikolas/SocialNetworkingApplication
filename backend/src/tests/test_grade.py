from fastapi.testclient import TestClient
import pytest
from app.factory import get_session, SESSION_LOCAL
from main import app
from .conftest import client
from sqlalchemy.orm import Session
from app.orm.user import UserModel
from httpx import Response
from app.services.grade import GradeService
from app.services.user import UserOrmService
from app.services.post import PostService

class TestGradeClass:
    email_user_1 = "tes1t@mail.ru"
    password_user_1 = 'test1'
    email_user_2 = "tes2t@mail.ru"
    password_user_2 = 'test2'
    user_1 = {
        "email": email_user_1,
        "password": password_user_1,
        "username": email_user_1,
    }
    user_2 = {
        "email": email_user_2,
        "password": password_user_2,
        "username": email_user_2,
    }

    def signup_user(self, client, db_session: Session, user:dict):
        response = client.post(app.url_path_for('create_user'), json=user)
        return response
    
    def login_user(self, client, db_session: Session, user:dict):
        response = client.post(app.url_path_for('login'), data=user, headers={ 'Content-Type': 'application/x-www-form-urlencoded'})
        return response
    
    def signup(self, client, db_session: Session):
        self.signup_user(client, db_session, TestGradeClass.user_1)
        resp_login_user1: Response = self.login_user(client, db_session, TestGradeClass.user_1)
        access_token_user_1 = resp_login_user1.json().get('access_token')

        self.signup_user(client, db_session, TestGradeClass.user_2)
        resp_login_user1: Response = self.login_user(client, db_session, TestGradeClass.user_2)
        access_token_user_2 = resp_login_user1.json().get('access_token')

        return access_token_user_1, access_token_user_2

    def test_like_post(self, client, db_session: Session):
        access_token_user_1, access_token_user_2 = self.signup(client, db_session)
        TEXT_POST_1,TEXT_POST_2 = 'test_post_1', 'test_post_2'
        response_create_post_1:Response = client.post(app.url_path_for('create_post'), json={"text": TEXT_POST_1}, headers={ 'Authorization': f'Bearer {access_token_user_1}'})
        response_create_post_2:Response = client.post(app.url_path_for('create_post'), json={"text": TEXT_POST_2}, headers={ 'Authorization': f'Bearer {access_token_user_2}'})
        assert response_create_post_1.status_code==200 and response_create_post_2.status_code==200

        response_like_post1_user1:Response = client.post(app.url_path_for('grade_post', post_id=response_create_post_1.json().get('id')) , json={'like': True},headers={ 'Authorization': f'Bearer {access_token_user_1}'})
        assert response_like_post1_user1.status_code!=200, response_like_post1_user1.status_code
       
        response_like_post1_user2:Response = client.post(app.url_path_for('grade_post', post_id=response_create_post_1.json().get('id')) , json={'like': True},headers={ 'Authorization': f'Bearer {access_token_user_2}'})
        assert response_like_post1_user2.status_code==200, response_like_post1_user2.status_code
        post1 = response_like_post1_user2.json()
        assert post1.get('is_author') is False
        assert post1.get('is_like') is True

    def test_delete_grade_post(self, client, db_session: Session):
        access_token_user_1, access_token_user_2 = self.signup(client, db_session)
        TEXT_POST_1,TEXT_POST_2 = 'test_post_1', 'test_post_2'
        response_create_post_1:Response = client.post(app.url_path_for('create_post'), json={"text": TEXT_POST_1}, headers={ 'Authorization': f'Bearer {access_token_user_1}'})
        assert response_create_post_1.status_code==200 

        response_like_post1_user1:Response = client.delete(app.url_path_for('delete_grade_post', post_id=response_create_post_1.json().get('id')) ,headers={ 'Authorization': f'Bearer {access_token_user_1}'})
        assert response_like_post1_user1.status_code==403, response_like_post1_user1.text

        response_like_post1_user2:Response = client.post(app.url_path_for('grade_post', post_id=response_create_post_1.json().get('id')) , json={'like': True},headers={ 'Authorization': f'Bearer {access_token_user_2}'})
        assert response_like_post1_user2.status_code==200, response_like_post1_user2.text


        response_delete_post1_user2:Response = client.delete(app.url_path_for('delete_grade_post', post_id=response_create_post_1.json().get('id')),headers={ 'Authorization': f'Bearer {access_token_user_2}'})
        assert response_delete_post1_user2.status_code==200, response_delete_post1_user2.text
       
        user = UserOrmService(db_session).get_user_by_email(TestGradeClass.email_user_1)
        assert GradeService(db_session, user).get(post=PostService(db_session, user).get(response_create_post_1.json().get('id'))) is None