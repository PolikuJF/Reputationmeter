from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class EstablishmentCreateByUrl(BaseModel):
    url: str

class EstablishmentBase(BaseModel):
    name: str
    address: Optional[str] = None
    platform_url: str
    platform_type: str
    external_id: Optional[str] = None

class EstablishmentCreate(EstablishmentBase):
    pass

class EstablishmentOut(EstablishmentBase):
    id: int
    owner_id: int
    is_archived: bool
    created_at: datetime
    last_parsed_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    establishment_id: int
    external_id: str
    author_name: Optional[str] = None
    rating: Optional[int] = None
    text: Optional[str] = None
    created_at_origin: Optional[datetime] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdateStatus(BaseModel):
    status: str

class ReviewOut(ReviewBase):
    id: int
    fetched_at: datetime
    sentiment: Optional[str] = None
    topics: Optional[str] = None
    is_processed: bool
    status: str
    notification_sent_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class ReviewsResponse(BaseModel):
    items: List[ReviewOut]
    total: int
