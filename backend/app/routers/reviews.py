from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import crud, schemas
from app.routers.auth import oauth2_scheme
from app.routers.establishments import get_current_user
from fastapi import BackgroundTasks
from app.tasks.analysis import process_review_async

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.get("/", response_model=List[schemas.ReviewOut])
def list_reviews(
    establishment_id: Optional[int] = Query(None),
    sentiment: Optional[str] = Query(None, regex="^(positive|neutral|negative)$"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    reviews = crud.get_reviews(db, establishment_id, sentiment, skip=offset, limit=limit)
    # TODO: добавить фильтрацию по owner_id через связанные заведения
    return reviews

@router.patch("/{review_id}/status", response_model=schemas.ReviewOut)
def update_status(review_id: int, update: schemas.ReviewUpdateStatus, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    review = crud.update_review_status(db, review_id, update.status)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    # TODO: проверить, что отзыв принадлежит заведению текущего пользователя
    return review

@router.post("/{review_id}/analyze")
def trigger_analysis(review_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    background_tasks.add_task(process_review_async, review_id)
    return {"status": "analysis started"}