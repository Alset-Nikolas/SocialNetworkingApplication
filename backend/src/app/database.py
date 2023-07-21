
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy_utils import create_database, database_exists, drop_database

def init_engine(database_url) -> Engine:
    return create_engine(database_url)

def init_metadata(naming_convention:dict)->MetaData:
    return MetaData(naming_convention=naming_convention)

def init_base(metadata: MetaData) -> DeclarativeMeta:
    return declarative_base(metadata=metadata)

def init_session(engine: Engine):
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)

def init_db(engine, Base):
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)

