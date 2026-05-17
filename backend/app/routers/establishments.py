from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import crud, schemas
from app.routers.auth import oauth2_scheme
from jose import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"

router = APIRouter(prefix="/establishments", tags=["establishments"])

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = crud.get_user_by_email(db, email)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/", response_model=List[schemas.EstablishmentOut])
def list_establishments(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return crud.get_establishments(db, owner_id=current_user.id)

@router.post("/", response_model=schemas.EstablishmentOut)
def add_establishment(est: schemas.EstablishmentCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # TODO: валидация URL через API Яндекс.Карт
    return crud.create_establishment(db, est, current_user.id)