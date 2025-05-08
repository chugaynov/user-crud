from fastapi import Depends
from sqlalchemy.orm import Session
from app.common.database import engine


def get_db():
    """
    Dependency for getting a database session.
    """
    with engine.get_session() as session:
        yield session
