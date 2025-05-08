import os
import contextlib
from app.common.singleton import Singleton
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config.settings import settings

DB_USER = os.getenv("DB_USER", settings.DB.USER)
DB_PASSWORD = os.getenv("DB_PASSWORD", settings.DB.PASSWORD)
DB_HOST = os.getenv("DB_HOST", settings.DB.HOST)
DB_NAME = os.getenv("DB_NAME", settings.DB.NAME)

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
# # NOT SECURED (local tests only)
# DATABASE_URL = f"postgresql://postgres:{DB_PASSWORD}@{DB_HOST}/appdb"

Base = declarative_base()


class Database(metaclass=Singleton):
    def __init__(self, database_url: str = DATABASE_URL):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @contextlib.contextmanager
    def get_session(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_engine(self):
        return self.engine
