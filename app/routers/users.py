from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.utils import hash_pasword


router = APIRouter(prefix="/users", tags=["Users"])


@router.post('/signup', response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    extisting_user = db.query(models.User).filter(models.User.email == user.email).first()
    if extisting_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_pw = hash_pasword(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_pw)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user