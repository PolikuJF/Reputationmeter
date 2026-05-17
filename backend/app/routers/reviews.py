from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import crud, schemas, models
from app.routers.auth import oauth2_scheme
from app.routers.establishments import get_current_user
from fastapi import BackgroundTasks
from app.tasks.analysis import process_review_async

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.get("", response_model=List[schemas.ReviewOut])
def list_reviews(
    establishment_id: Optional[int] = Query(None),
    sentiment: Optional[str] = Query(None, regex="^(positive|neutral|negative)$"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Безопасность: показываем только отзывы, принадлежащие заведениям текущего владельца
    query = db.query(models.Review).join(models.Establishment).filter(
        models.Establishment.owner_id == current_user.id
    )
    
    if establishment_id:
        # Дополнительно проверяем, что заведение принадлежит пользователю
        est = db.query(models.Establishment).filter(
            models.Establishment.id == establishment_id,
            models.Establishment.owner_id == current_user.id
        ).first()
        if not est:
            raise HTTPException(status_code=404, detail="Establishment not found or access denied")
        query = query.filter(models.Review.establishment_id == establishment_id)
    
    if sentiment:
        query = query.filter(models.Review.sentiment == sentiment)
    
    # Пагинация
    reviews = query.offset(offset).limit(limit).all()
    return reviews

@router.patch("/{review_id}/status", response_model=schemas.ReviewOut)
def update_status(
    review_id: int,
    update: schemas.ReviewUpdateStatus,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Проверяем, что отзыв принадлежит заведению текущего пользователя
    review = db.query(models.Review).join(models.Establishment).filter(
        models.Review.id == review_id,
        models.Establishment.owner_id == current_user.id
    ).first()
    
    if not review:
        raise HTTPException(status_code=404, detail="Review not found or access denied")
    
    updated_review = crud.update_review_status(db, review_id, update.status)
    return updated_review

@router.post("/{review_id}/analyze")
def trigger_analysis(
    review_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Проверяем права доступа
    review = db.query(models.Review).join(models.Establishment).filter(
        models.Review.id == review_id,
        models.Establishment.owner_id == current_user.id
    ).first()
    
    if not review:
        raise HTTPException(status_code=404, detail="Review not found or access denied")
    
    background_tasks.add_task(process_review_async, review_id)
    return {"status": "analysis started"}

@router.get("/unnotified")
def get_unnotified_negative_reviews(
    sentiment: str = Query("negative"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Только негативные отзывы, без уведомлений, принадлежащие заведениям пользователя
    reviews = db.query(models.Review).join(models.Establishment).filter(
        models.Establishment.owner_id == current_user.id,
        models.Review.sentiment == sentiment,
        models.Review.notification_sent_at.is_(None)
    ).all()
    return reviews