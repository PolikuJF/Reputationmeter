from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

<<<<<<< HEAD
=======
# User
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
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
<<<<<<< HEAD
    class Config:
        from_attributes = True

=======

    class Config:
        from_attributes = True

# Token
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

<<<<<<< HEAD
class EstablishmentCreateByUrl(BaseModel):
    url: str

=======
# Establishment
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
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
<<<<<<< HEAD
    class Config:
        from_attributes = True

=======

    class Config:
        from_attributes = True

# Review
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
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
<<<<<<< HEAD
    status: str
=======
    status: str  # 'new', 'acknowledged', 'resolved'
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1

class ReviewOut(ReviewBase):
    id: int
    fetched_at: datetime
    sentiment: Optional[str] = None
<<<<<<< HEAD
    topics: Optional[str] = None
    is_processed: bool
    status: str
    notification_sent_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class ReviewsResponse(BaseModel):
    items: List[ReviewOut]
    total: int
=======
    topics: Optional[str] = None  # JSON string
    is_processed: bool
    status: str
    notification_sent_at: Optional[datetime] = None

    class Config:
        from_attributes = True
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
