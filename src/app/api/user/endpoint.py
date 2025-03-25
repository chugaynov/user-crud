import os
from fastapi import APIRouter, HTTPException, Depends
from app.api.user.response import User, UserCreate, UserResponse
from app.common.database import Database
from app.config.settings import settings

router = APIRouter()

DB_USER = os.getenv("DB_USER", settings.DB.USER)
DB_PASSWORD = os.getenv("DB_PASSWORD", settings.DB.PASSWORD)
DB_HOST = os.getenv("DB_HOST", settings.DB.HOST)
DB_NAME = os.getenv("DB_NAME", settings.DB.NAME)

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

db_instance = Database(DATABASE_URL)


def get_db():
    db = db_instance.get_session()
    try:
        yield db
    finally:
        db.close()


@router.post("/user", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db=Depends(get_db)):
    db_user = User(
        username=user.username,
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        phone=user.phone,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/user/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/user/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserCreate, db=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = updated_user.username
    user.firstName = updated_user.firstName
    user.lastName = updated_user.lastName
    user.email = updated_user.email
    user.phone = updated_user.phone
    db.commit()
    db.refresh(user)
    return user


@router.delete("/user/{user_id}", status_code=204)
def delete_user(user_id: int, db=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
