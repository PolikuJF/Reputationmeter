from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from app.routers.establishments import get_current_user
from app.services.parsing_service import run_parsing_for_establishment

router = APIRouter(prefix="/parsing", tags=["parsing"])

@router.post("/establishments/{establishment_id}/run")
async def run_parser(establishment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    establishment = db.query(models.Establishment).filter(
        models.Establishment.id == establishment_id,
        models.Establishment.owner_id == current_user.id,
        models.Establishment.is_archived == False,
    ).first()
    if not establishment:
        raise HTTPException(status_code=404, detail="Заведение не найдено")
    return run_parsing_for_establishment(db, establishment)
