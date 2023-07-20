from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

metadata = MetaData(naming_convention=settings.DATABASE_NAMING_CONVENTIONS)
Base = declarative_base(metadata=metadata, bind=engine)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

