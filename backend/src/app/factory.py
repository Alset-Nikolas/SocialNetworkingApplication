import os
import typing as t
from fastapi import FastAPI
from passlib.context import CryptContext
import app.core.settings
from app.init_utils import get_app_config_from_environ, init_settings
from app.database import init_engine, init_metadata, init_session, init_base, init_db
from app.core.config import AppDevelopmentSettings,AppProductionSettings, AppTestSettings




APP_CONFIG_NAME:str = get_app_config_from_environ()
SETTINGS:t.Union[AppDevelopmentSettings,AppProductionSettings, AppTestSettings] = init_settings(APP_CONFIG_NAME)
ENGINE = init_engine(SETTINGS.DATABASE_URL)
META_DATA = init_metadata(SETTINGS.DATABASE_NAMING_CONVENTIONS)
BASE = init_base(metadata=META_DATA)
SESSION_LOCAL = init_session(engine=ENGINE)
PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_app():
    app:FastAPI = FastAPI()
    init_db(engine=ENGINE, Base=BASE)
    setup_routers(app)
    return app

def setup_routers(app: FastAPI):
    from app.api import api_router
    app.include_router(api_router, prefix=SETTINGS.API_PATH)

def get_session() -> t.Generator:
    db = SESSION_LOCAL()  
    try:
        yield db 
    finally:
        db.close()  