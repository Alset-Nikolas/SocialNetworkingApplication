from fastapi.testclient import TestClient
import pytest
from app.factory import get_session, SESSION_LOCAL
from main import app
from .conftest import client
from sqlalchemy.orm import Session
from app.orm.user import UserModel
from app.services.user import UserOrmService
from app.services.post import PostService
from httpx import Response
import typing as t

class TestPostClass:
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
        self.signup_user(client, db_session, TestPostClass.user_1)
        resp_login_user1: Response = self.login_user(client, db_session, TestPostClass.user_1)
        access_token_user_1 = resp_login_user1.json().get('access_token')

        self.signup_user(client, db_session, TestPostClass.user_2)
        resp_login_user1: Response = self.login_user(client, db_session, TestPostClass.user_2)
        access_token_user_2 = resp_login_user1.json().get('access_token')

        return access_token_user_1, access_token_user_2

    
    def test_create_post(self, client, db_session: Session):
        TEXT_POST = 'test_post'
        access_token_user_1, access_token_user_2 = self.signup(client, db_session)
        response_post:Response = client.post(app.url_path_for('create_post'), json={"text": TEXT_POST}, headers={ 'Authorization': f'Bearer {access_token_user_1}'})
        assert response_post.status_code == 200, response_post.text
        data = response_post.json()
        assert data.get('is_like') == None, data.get('is_like') 
        assert data.get('is_author'), data.get('is_author')
        assert data.get('text') == TEXT_POST, data.get('text')

    def test_list_post(self, client, db_session: Session):
        access_token_user_1, access_token_user_2 = self.signup(client, db_session)
        TEXT_POST_1,TEXT_POST_2 = 'test_post_1', 'test_post_2'
        response_create_post_1:Response = client.post(app.url_path_for('create_post'), json={"text": TEXT_POST_1}, headers={ 'Authorization': f'Bearer {access_token_user_1}'})
        response_create_post_2:Response = client.post(app.url_path_for('create_post'), json={"text": TEXT_POST_2}, headers={ 'Authorization': f'Bearer {access_token_user_2}'})
        assert response_create_post_1.status_code==200 and response_create_post_2.status_code==200

        response_list_post_1:Response = client.get(app.url_path_for('get_list_post') ,headers={ 'Authorization': f'Bearer {access_token_user_1}'})
        assert response_list_post_1.status_code==200, response_list_post_1.status_code
        posts:t.List = response_list_post_1.json()
        assert len(posts) == 2, len(posts)
        POST1_INFO_BY_USER1 ={
            "id": response_create_post_1.json().get('id'),
            "text": TEXT_POST_1,
            "date":response_create_post_1.json().get('date') ,
            "author_email": TestPostClass.user_1.get('email'),
            "is_author": True,
            "is_like": None
        }
        POST2_INFO_BY_USER1 ={
            "id": response_create_post_2.json().get('id'),
            "text": TEXT_POST_2,
            "date":response_create_post_2.json().get('date') ,
            "author_email": TestPostClass.user_2.get('email'),
            "is_author": False,
            "is_like": None
        }
        assert any(p==POST1_INFO_BY_USER1 for p in posts)
        assert any(p==POST2_INFO_BY_USER1 for p in posts)

    def test_get_post(self, client, db_session: Session):
        access_token_user_1, _ = self.signup(client, db_session)
        TEXT_POST_1 = 'test_post_1'
        response_create_post_1:Response = client.post(app.url_path_for('create_post'), json={"text": TEXT_POST_1}, headers={ 'Authorization': f'Bearer {access_token_user_1}'})
        assert response_create_post_1.status_code==200
        response_post_1:Response = client.get(app.url_path_for('get_post', post_id= response_create_post_1.json().get('id')), headers={ 'Authorization': f'Bearer {access_token_user_1}'})
        assert response_post_1.status_code == 200
        assert response_post_1.json().get('text') == TEXT_POST_1

    def test_delete_post(self, client, db_session: Session):
        access_token_user_1, access_token_user_2 = self.signup(client, db_session)
        TEXT_POST_1 = 'test_post_1'
        response_create_post_1:Response = client.post(app.url_path_for('create_post'), json={"text": TEXT_POST_1}, headers={ 'Authorization': f'Bearer {access_token_user_1}'})
        assert response_create_post_1.status_code==200

        response_detele_post1_user2:Response = client.delete(app.url_path_for('delete_post', post_id= response_create_post_1.json().get('id')), headers={ 'Authorization': f'Bearer {access_token_user_2}'})
        assert response_detele_post1_user2.status_code == 403

        response_detele_post1_user1:Response = client.delete(app.url_path_for('delete_post', post_id= response_create_post_1.json().get('id')), headers={ 'Authorization': f'Bearer {access_token_user_1}'})
        assert response_detele_post1_user1.status_code == 200

        assert PostService(db_session, None).get(response_create_post_1.json().get('id')) is None