from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app import models, schemas
from app.routers.auth import oauth2_scheme
from app.routers.establishments import get_current_user
from datetime import datetime, timedelta
from collections import defaultdict

router = APIRouter(prefix="/dashboard", tags=["dashboard"],)

@router.get("/overview")
def get_overview(
    establishment_id: Optional[int] = Query(None),
    from_date: Optional[str] = Query(None),
    to_date: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Базовый запрос отзывов (только для заведений текущего пользователя)
    query = db.query(models.Review).join(models.Establishment).filter(
        models.Establishment.owner_id == current_user.id
    )
    
    if establishment_id:
        query = query.filter(models.Review.establishment_id == establishment_id)
    
    # Фильтр по дате, если указана
    if from_date:
        try:
            from_dt = datetime.fromisoformat(from_date)
            query = query.filter(models.Review.created_at_origin >= from_dt)
        except:
            pass
    if to_date:
        try:
            to_dt = datetime.fromisoformat(to_date) + timedelta(days=1)
            query = query.filter(models.Review.created_at_origin < to_dt)
        except:
            pass
    
    reviews = query.all()
    
    total_reviews = len(reviews)
    positive = sum(1 for r in reviews if r.sentiment == 'positive')
    neutral = sum(1 for r in reviews if r.sentiment == 'neutral')
    negative = sum(1 for r in reviews if r.sentiment == 'negative')
    
    # Простейшая временная разбивка (по дням)
    timeline_dict = defaultdict(lambda: {"positive": 0, "neutral": 0, "negative": 0})
    for r in reviews:
        if r.created_at_origin:
            date_str = r.created_at_origin.date().isoformat()
            if r.sentiment == 'positive':
                timeline_dict[date_str]["positive"] += 1
            elif r.sentiment == 'neutral':
                timeline_dict[date_str]["neutral"] += 1
            elif r.sentiment == 'negative':
                timeline_dict[date_str]["negative"] += 1
    
    timeline = [{"date": k, **v} for k, v in sorted(timeline_dict.items())]
    
    # Топ темы (упрощённо: собираем все темы из отзывов)
    topics_counter = defaultdict(int)
    for r in reviews:
        if r.topics:
            # topics может быть строкой, разделённой запятыми, или списком
            try:
                import json
                topics_list = json.loads(r.topics) if isinstance(r.topics, str) else r.topics
                if isinstance(topics_list, list):
                    for t in topics_list:
                        topics_counter[t] += 1
            except:
                if isinstance(r.topics, str):
                    for t in r.topics.split(','):
                        topics_counter[t.strip()] += 1
    
    top_topics = [t for t, _ in sorted(topics_counter.items(), key=lambda x: x[1], reverse=True)[:10]]
    
    return {
        "total_reviews": total_reviews,
        "positive_percent": round(positive / total_reviews * 100, 1) if total_reviews else 0,
        "neutral_percent": round(neutral / total_reviews * 100, 1) if total_reviews else 0,
        "negative_percent": round(negative / total_reviews * 100, 1) if total_reviews else 0,
        "sentiment_timeline": timeline,
        "top_topics": top_topics
    }
@router.get("/ping")
def ping():
    return {"status": "ok"}