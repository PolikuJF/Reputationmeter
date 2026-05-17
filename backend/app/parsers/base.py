from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ParsedReview:
    external_id: str
    author_name: Optional[str]
    rating: Optional[int]
    text: Optional[str]
    created_at_origin: Optional[datetime]

class BaseParser(ABC):
    @abstractmethod
    def parse_reviews(self, establishment) -> list[ParsedReview]:
        pass
