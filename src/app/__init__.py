import os
import warnings
import typing as t
from dotenv import load_dotenv
from fastapi import FastAPI
from app.init_utils import get_app_config_from_environ, init_settings
from app.core.config import AppDevelopmentSettings,AppProductionSettings, AppTestSettings
from app.database import init_engine, init_metadata, init_session, init_base, init_db



APP_CONFIG_NAME:str = get_app_config_from_environ()
SETTINGS:t.Union[AppDevelopmentSettings,AppProductionSettings, AppTestSettings] = init_settings(APP_CONFIG_NAME)
ENGINE = init_engine(SETTINGS.DATABASE_URL)
META_DATA = init_metadata(SETTINGS.DATABASE_NAMING_CONVENTIONS)
BASE = init_base(metadata=META_DATA)
SESSION_LOCAL = init_session(engine=ENGINE)



def create_app():
    
    app:FastAPI = FastAPI()
    init_db(engine=ENGINE, Base=BASE)
    setup_routers(app)
    # init_extensions(app)
    # register_blueprints(app)
    # register_apispec(app, spec)
    # migrate.init_app(app, db)
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