from fastapi import APIRouter, HTTPException, Depends

from app.api.user.models import User
from app.api.user.schemas import UserScheme, UserIdScheme

from sqlalchemy.exc import IntegrityError
from app.common.database import Database



router = APIRouter()


def get_db():
    with Database().get_session() as session:
        yield session


@router.post("/user", response_model=UserIdScheme, status_code=201)
def create_user(user: UserScheme, db=Depends(get_db)) -> UserIdScheme:
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
        return {
            "id": db_user.id
        }
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


@router.get("/user/{user_id}", response_model=UserScheme)
def get_user(user_id: int, db=Depends(get_db)) -> UserScheme:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user


@router.put("/user/{user_id}", response_model=UserScheme)
def update_user(user_id: int, updated_user: UserScheme, db=Depends(get_db)) -> UserScheme:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update only existed user parameters
    user_data = updated_user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)

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
