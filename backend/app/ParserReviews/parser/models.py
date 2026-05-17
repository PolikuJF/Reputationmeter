from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    establishment_id = Column(Integer, ForeignKey("establishments.id", ondelete="CASCADE"))
    external_id = Column(String(255), unique=True, nullable=False)
    author_name = Column(String(255))
    rating = Column(Integer)
    text = Column(Text)
    created_at_origin = Column(DateTime)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    sentiment = Column(String(20))
    topics = Column(Text)  # JSON
    is_processed = Column(Boolean, default=False)
    status = Column(String(20), default="new")
    notification_sent_at = Column(DateTime)