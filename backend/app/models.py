from sqlalchemy import String, Integer, Boolean, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class Establishment(Base):
    __tablename__ = "establishments"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(Text)
    platform_url: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    platform_type: Mapped[str] = mapped_column(String(20), nullable=False)
    external_id: Mapped[Optional[str]] = mapped_column(String(100))
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_parsed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    establishment_id: Mapped[int] = mapped_column(ForeignKey("establishments.id", ondelete="CASCADE"))
    external_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    author_name: Mapped[Optional[str]] = mapped_column(String(255))
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    text: Mapped[Optional[str]] = mapped_column(Text)
    created_at_origin: Mapped[Optional[datetime]] = mapped_column(DateTime)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    sentiment: Mapped[Optional[str]] = mapped_column(String(20))
    topics: Mapped[Optional[list]] = mapped_column(Text)  # будет хранить JSON строку
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(20), default="new")
    notification_sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    __table_args__ = (
        CheckConstraint("sentiment IN ('positive','neutral','negative')", name="check_sentiment"),
        CheckConstraint("status IN ('new','acknowledged','resolved')", name="check_status"),
    )

class ParsingLog(Base):
    __tablename__ = "parsing_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    establishment_id: Mapped[int] = mapped_column(ForeignKey("establishments.id"))
    started_at: Mapped[datetime] = mapped_column(DateTime)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(20))
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    reviews_fetched: Mapped[Optional[int]] = mapped_column(Integer)
    proxy_used: Mapped[Optional[str]] = mapped_column(String(100))