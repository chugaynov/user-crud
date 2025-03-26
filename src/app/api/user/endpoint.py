import os
from fastapi import APIRouter, HTTPException, Depends
from app.api.user.response import User, UserCreate, UserResponse
from app.common.database import Database
from app.config.settings import settings
from sqlalchemy.exc import IntegrityError  # Импортируем исключение SQLAlchemy

router = APIRouter()

DB_USER = os.getenv("DB_USER", settings.DB.USER)
DB_PASSWORD = os.getenv("DB_PASSWORD", settings.DB.PASSWORD)
DB_HOST = os.getenv("DB_HOST", settings.DB.HOST)
DB_NAME = os.getenv("DB_NAME", settings.DB.NAME)

# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
DATABASE_URL = f"postgresql://postgres:{DB_PASSWORD}@{DB_HOST}/appdb"

db_instance = Database(DATABASE_URL)


def get_db():
    db = db_instance.get_session()
    try:
        yield db
    finally:
        db.close()


@router.post("/user", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db=Depends(get_db)):
    try:
        db_user = User(
            userName=user.userName,
            firstName=user.firstName,
            lastName=user.lastName,
            email=user.email,
            phone=user.phone,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="User with this username or email already exists"
        )
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=502,
            detail="An unexpected error occurred while processing the request"
        )

@router.get("/user/{user_name}", response_model=UserResponse)
def get_user(user_name: str, db=Depends(get_db)):
    user = db.query(User).filter(User.userName == user_name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/user/{user_name}", response_model=UserResponse)
def update_user(user_name: str, updated_user: UserCreate, db=Depends(get_db)):
    user = db.query(User).filter(User.userName == user_name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.userName = updated_user.userName
    user.firstName = updated_user.firstName
    user.lastName = updated_user.lastName
    user.email = updated_user.email
    user.phone = updated_user.phone
    db.commit()
    db.refresh(user)
    return user


@router.delete("/user/{user_name}", status_code=204)
def delete_user(user_name: str, db=Depends(get_db)):
    user = db.query(User).filter(User.userName == user_name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
