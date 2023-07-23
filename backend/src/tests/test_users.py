from fastapi.testclient import TestClient
import pytest
from app.factory import get_session, SESSION_LOCAL
from main import app
from .conftest import client
from sqlalchemy.orm import Session
from app.orm.user import UserModel
from app.services.user import UserOrmService
from httpx import Response

class TestUserClass:
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

    def signup_user1(self, client, db_session: Session):
        response = client.post(app.url_path_for('create_user'), json=TestUserClass.user_1)
        return response

    def test_signup(self, client, db_session: Session):
        n = len(UserOrmService(db_session).get_all())
        assert UserOrmService(db_session).get_user_by_email(TestUserClass.user_1.get('email')) is None
        response = client.post(app.url_path_for('create_user'), json=TestUserClass.user_1)
        assert response.status_code == 200
        assert UserOrmService(db_session).get_user_by_email(TestUserClass.user_1.get('email')) is not None
        assert len(UserOrmService(db_session).get_all()) == n + 1

    def test_login(self, client, db_session: Session):
        self.signup_user1(client, db_session)
        response = client.post(app.url_path_for('login'), data=TestUserClass.user_1, headers={ 'Content-Type': 'application/x-www-form-urlencoded'})
        assert response.status_code == 200, 'login err'
        assert 'access_token' in response.json()

    def test_signup_err(self, client, db_session: Session):
        resp: Response = self.signup_user1(client, db_session)
        resp2: Response = self.signup_user1(client, db_session)
        assert resp.status_code == 200 and resp2.status_code != 200

    def test_login_err(self, client, db_session: Session):
        self.signup_user1(client, db_session)
        response: Response = client.post(app.url_path_for('login'), data=TestUserClass.user_2)
        assert response.status_code != 200
