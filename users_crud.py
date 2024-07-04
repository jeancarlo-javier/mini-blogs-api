from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import User
import auth
import schemas

def create_user(db: Session, user: schemas.UserCreate) -> schemas.UserCreate:
    if auth.get_user_by_email(db, user.email):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="An user with this email is already created.")
    
    if len(user.password.get_secret_value()) < 8:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Password is too short")
    
    hashed_password = auth.hash_password(user.password.get_secret_value())

    new_user = User(name=user.name, email=user.email, password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return { "id": new_user.id, "name": new_user.name, "email": new_user.email }

def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user

def get_users(db: Session) -> list:
    result = db.query(User).all()

    return list(map(lambda user: {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }, result))