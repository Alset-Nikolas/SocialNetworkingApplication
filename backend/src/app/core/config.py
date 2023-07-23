import os
import typing as t
from pydantic_settings import BaseSettings
from functools import lru_cache


class Config(BaseSettings):
    DEBUG:bool = False
    TESTING:bool = False
    SECRET_KEY: str = os.environ["SECRET_KEY"]
    ALGORITHM:str="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int=30
    REFRESH_TOKEN_EXPIRE_MINUTES:int = 60 * 24 * 7 # 7 days
    JWT_SECRET_KEY:str = os.environ['JWT_SECRET_KEY']   # should be kept secret
    JWT_REFRESH_SECRET_KEY:str = os.environ['JWT_REFRESH_SECRET_KEY']    # should be kept secret


class Testing(Config):
    SETTINGS_NAME: str = 'test'
    TESTING: bool = True
    DATABASE_URL: str = (
        "postgresql+psycopg2://postgres:qwerty@localhost:5432"
        "/test_social_network_db"
    )


class Development(Config):
    SETTINGS_NAME: str = 'dev'
    DEBUG: bool = True
    DATABASE_URL: str = (
        "postgresql+psycopg2://postgres:qwerty@localhost:5432/social_network_db"
    )


class Production(Config):
    SETTINGS_NAME: str = 'prod'
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql+psycopg2://social_network:social_network@social_network_postgres:5432/social_network_db"


class AppBaseSettings(BaseSettings):
    PROJECT_NAME: str = "SocialNerworkApi"
    API_PATH: str = '/api/v1'

    DATABASE_NAMING_CONVENTIONS: t.Dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


class AppTestSettings(AppBaseSettings, Testing):
    pass


class AppDevelopmentSettings(AppBaseSettings, Development):
    pass


class AppProductionSettings(AppBaseSettings, Production):
    pass


settings_by_name = dict(dev=AppDevelopmentSettings, prod=AppProductionSettings, test=AppTestSettings)


@lru_cache()
def get_settings(name: str):
    settings: AppBaseSettings = settings_by_name[name]
    return settings()
