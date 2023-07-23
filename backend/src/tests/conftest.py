import pytest
import typing as t
from app.database import init_db, drop_db
from app.factory import BASE, ENGINE, SESSION_LOCAL, get_session, create_app
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture(scope="function")
def app() -> t.Generator[FastAPI, t.Any, None]:
    """
    Create a fresh database on each test case.
    """
    BASE.metadata.create_all(ENGINE)  # Create the tables.
    _app = create_app()
    yield _app
    BASE.metadata.drop_all(ENGINE)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> t.Generator[SESSION_LOCAL, t.Any, None]:
    connection = ENGINE.connect()
    # transaction = connection.begin()
    session = SESSION_LOCAL(bind=connection)
    yield session
    session.close()
    # transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
        app: FastAPI, db_session: SESSION_LOCAL
) -> t.Generator[TestClient, t.Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_session] = _get_test_db
    with TestClient(app) as client:
        yield client

# @pytest.fixture()
# def test_db():
#     init_db(ENGINE, BASE)
#     yield next(get_session())
#     drop_db(ENGINE, BASE)
