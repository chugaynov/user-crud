from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Модель данных
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), unique=True, index=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)

# Pydantic модель
class UserCreate(BaseModel):
    username: str = Field(..., max_length=256)
    firstName: str
    lastName: str
    email: EmailStr
    phone: str


class UserResponse(UserCreate):
    id: int
