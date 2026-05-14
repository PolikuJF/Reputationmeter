from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
from typing import Optional, List

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        role="owner",
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user

# Establishments
def get_establishments(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Establishment).filter(
        models.Establishment.owner_id == owner_id,
        models.Establishment.is_archived == False
    ).offset(skip).limit(limit).all()

def create_establishment(db: Session, est: schemas.EstablishmentCreate, owner_id: int):
    db_est = models.Establishment(**est.dict(), owner_id=owner_id)
    db.add(db_est)
    db.commit()
    db.refresh(db_est)
    return db_est

# Reviews
def get_reviews(db: Session, establishment_id: Optional[int] = None, sentiment: Optional[str] = None,
                skip: int = 0, limit: int = 100):
    query = db.query(models.Review)
    if establishment_id:
        query = query.filter(models.Review.establishment_id == establishment_id)
    if sentiment:
        query = query.filter(models.Review.sentiment == sentiment)
    return query.offset(skip).limit(limit).all()

def update_review_status(db: Session, review_id: int, status: str):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review:
        review.status = status
        db.commit()
        db.refresh(review)
    return review
def update_review_analysis(db: Session, review_id: int, sentiment: str, topics: list):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review:
        review.sentiment = sentiment
        review.topics = str(topics) if topics else None
        review.is_processed = True
        db.commit()
        db.refresh(review)
    return review

def get_establishment_owner_email(db: Session, establishment_id: int) -> str | None:
    est = db.query(models.Establishment).filter(models.Establishment.id == establishment_id).first()
    if est and est.owner:
        return est.owner.email
    return None