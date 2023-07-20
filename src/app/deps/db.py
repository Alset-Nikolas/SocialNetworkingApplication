from typing import Generator

from src.app.database import SessionLocal  


def get_session() -> Generator:
    db = SessionLocal()  
    try:
        yield db 
    finally:
        db.close()  
