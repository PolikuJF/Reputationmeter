from app.database import SessionLocal
from app import crud
from app.nlp.mock_nlp import analyze_sentiment, extract_topics
from app.email.sender import send_negative_review_notification

def process_review_async(review_id: int):
    db = SessionLocal()
    try:
        review = db.query(...).filter(models.Review.id == review_id).first()
        if not review or review.is_processed:
            return
        
        sentiment = analyze_sentiment(review.text or "")
        topics = extract_topics(review.text or "")
        
        crud.update_review_analysis(db, review_id, sentiment, topics)
        
        if sentiment == "negative":
            owner_email = crud.get_establishment_owner_email(db, review.establishment_id)
            if owner_email:
                establishment = db.query(models.Establishment).filter(models.Establishment.id == review.establishment_id).first()
                send_negative_review_notification(owner_email, establishment.name, review.text)
    finally:
        db.close()