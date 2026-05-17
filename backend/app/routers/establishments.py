<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from jose import jwt, JWTError
import os
from app.database import get_db
from app import crud, schemas, models
from app.routers.auth import oauth2_scheme
from app.services.establishment_resolver import resolve_establishment_by_url

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
router = APIRouter(prefix="/establishments", tags=["establishments"])

=======
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import crud, schemas
from app.routers.auth import oauth2_scheme
from jose import jwt
import os
from jose import JWTError

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"

router = APIRouter(prefix="/establishments", tags=["establishments"], )
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
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
<<<<<<< HEAD
async def list_establishments(active_only: bool = Query(True), db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    query = db.query(models.Establishment).filter(models.Establishment.owner_id == current_user.id)
    if active_only:
        query = query.filter(models.Establishment.is_archived == False)
    return query.order_by(models.Establishment.created_at.desc()).all()

@router.post("", response_model=schemas.EstablishmentOut)
async def add_establishment(payload: schemas.EstablishmentCreateByUrl, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    data = await resolve_establishment_by_url(payload.url)
    exists = db.query(models.Establishment).filter(models.Establishment.owner_id == current_user.id, models.Establishment.platform_url == data["platform_url"]).first()
    if exists:
        raise HTTPException(status_code=400, detail="Заведение уже добавлено")
    est = schemas.EstablishmentCreate(**data)
    return crud.create_establishment(db, est, current_user.id)

@router.delete("/{establishment_id}")
async def archive_establishment(establishment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    establishment = db.query(models.Establishment).filter(models.Establishment.id == establishment_id, models.Establishment.owner_id == current_user.id).first()
    if not establishment:
        raise HTTPException(status_code=404, detail="Заведение не найдено")
    establishment.is_archived = True
    db.commit()
    return {"status": "archived"}
=======
def list_establishments(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return crud.get_establishments(db, owner_id=current_user.id)

@router.post("", response_model=schemas.EstablishmentOut)
def add_establishment(est: schemas.EstablishmentCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # TODO: валидация URL через API Яндекс.Карт
    return crud.create_establishment(db, est, current_user.id)
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
