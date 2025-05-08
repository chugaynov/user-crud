from sqlalchemy import Column, Integer, String

from app.common.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    userName = Column("user_name", String(256), unique=True, index=True)
    firstName = Column("first_name", String(256), nullable=False)
    lastName = Column("last_name", String(256), nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    phone = Column(String(256), nullable=False)


