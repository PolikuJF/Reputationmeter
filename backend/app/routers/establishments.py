from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from jose import jwt, JWTError
import os
from urllib.parse import urlparse
from app.database import get_db
from app import crud, schemas, models
from app.routers.auth import oauth2_scheme

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

@router.get("", response_model=List[schemas.EstablishmentOut])
async def list_establishments(active_only: bool = Query(True), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    query = db.query(models.Establishment).filter(models.Establishment.owner_id == current_user.id)
    if active_only:
        query = query.filter(models.Establishment.is_archived == False)
    return query.order_by(models.Establishment.created_at.desc()).all()


@router.post("", response_model=schemas.EstablishmentOut)
async def add_establishment(payload: schemas.EstablishmentCreateManual, db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    parsed = urlparse(payload.url)
    host = parsed.netloc.lower()
    if "yandex" in host:
        platform_type = "yandex"
    elif "google" in host or "goo.gl" in host:
        platform_type = "google"
    elif "2gis" in host:
        platform_type = "2gis"
    else:
        raise HTTPException(status_code=400, detail="Поддерживаются ссылки Яндекс.Карт, Google Maps или 2ГИС")
    

    exists = db.query(models.Establishment).filter(
        models.Establishment.owner_id == current_user.id,
        models.Establishment.platform_url == payload.url
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Заведение уже добавлено")
    

    est = schemas.EstablishmentCreate(
        name=payload.name,
        address=payload.address,
        platform_url=payload.url,
        platform_type=platform_type,
        external_id=None
    )
    return crud.create_establishment(db, est, current_user.id)

@router.delete("/{establishment_id}")
async def archive_establishment(establishment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    establishment = db.query(models.Establishment).filter(models.Establishment.id == establishment_id, models.Establishment.owner_id == current_user.id).first()
    if not establishment:
        raise HTTPException(status_code=404, detail="Заведение не найдено")
    establishment.is_archived = True
    db.commit()
    return {"status": "archived"}