from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from infrastructure.database.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# database dependency for FastAPI
db_dependency = Annotated[Session, Depends(get_db)]