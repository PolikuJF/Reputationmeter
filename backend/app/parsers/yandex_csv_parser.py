import csv
import hashlib
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.parsers.base import BaseParser, ParsedReview


class YandexCsvParser(BaseParser):
    def __init__(self, csv_path: str | None = None):
        self.csv_path = Path(csv_path or "app/ParserReviews/csv/Rolls.csv")

    def parse_reviews(self, establishment) -> list[ParsedReview]:
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        reviews: list[ParsedReview] = []

        with self.csv_path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                raw_text = self._get_raw_text(row)

                author = self._extract_author(row)
                text = self._extract_text(row, author)
                rating = self._extract_rating(row)
                created_at = self._extract_date(row, raw_text)

                if not text or len(text.strip()) < 25:
                    continue

                if len(text.split()) < 4:
                    continue

                external_source = (
                    row.get("external_id")
                    or row.get("selenium_id")
                    or f"{author}:{rating}:{created_at}:{text}"
                )

                external_id = hashlib.sha256(
                    f"{establishment.id}:{external_source}".encode("utf-8")
                ).hexdigest()

                reviews.append(
                    ParsedReview(
                        external_id=external_id,
                        author_name=author,
                        rating=rating,
                        text=text,
                        created_at_origin=created_at,
                    )
                )

        return reviews

    def _get_raw_text(self, row: dict) -> str:
        return str(
            row.get("review_text")
            or row.get("text")
            or row.get("comment")
            or row.get("review")
            or ""
        )

    def _extract_text(self, row: dict, author: str = "unknown") -> str:
        text = self._get_raw_text(row)

        garbage_patterns = [
            r"Знаток города\s+\d+\s+уровня",
            r"Level\s+\d+\s+Local Expert",
            r"Подписаться",
            r"Subscribe",
            r"Посмотреть ответ организации",
            r"Скрыть ответ организации",
            r"Show business's response",
            r"Hide business's response",
            r"Show business response",
            r"Hide business response",
            r"\bmore\b",
        ]

        for pattern in garbage_patterns:
            text = re.sub(pattern, " ", text, flags=re.IGNORECASE)

        text = re.sub(
            r"\b\d{1,2}\s+"
            r"(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)"
            r"(?:\s+\d{4})?\b",
            " ",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"\b"
            r"(January|February|March|April|May|June|July|August|September|October|November|December)"
            r"\s+\d{1,2},?\s*\d{4}?\b",
            " ",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(r"\[None,\s*'[^']+'\]", " ", text)

        if author and author != "unknown":
            text = re.sub(
                rf"^\s*{re.escape(author)}\s*",
                "",
                text,
                flags=re.IGNORECASE,
            )

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def _extract_author(self, row: dict) -> str:
        source = " ".join(str(v) for v in row.values() if v)

        match = re.search(r"\[None,\s*'([^']+)'\]", source)
        if match:
            return match.group(1).strip()

        match = re.search(r"name:\s*\[None,\s*'([^']+)'\]", source)
        if match:
            return match.group(1).strip()

        return "unknown"

    def _extract_rating(self, row: dict) -> Optional[int]:
        raw_rating = (
            row.get("review_rating")
            or row.get("rating")
            or row.get("score")
            or row.get("stars")
            or ""
        )

        raw_rating = str(raw_rating).strip()

        if raw_rating.isdigit():
            rating = int(raw_rating)
            return rating if 1 <= rating <= 5 else None

        match = re.search(r"\b([1-5])\b", raw_rating)
        if match:
            return int(match.group(1))

        source = " ".join(str(v) for v in row.values() if v)

        patterns = [
            r"rating['\"]?\s*[:=]\s*['\"]?([1-5])",
            r"оценка['\"]?\s*[:=]\s*['\"]?([1-5])",
            r"stars['\"]?\s*[:=]\s*['\"]?([1-5])",
            r"([1-5])\s*(?:звезд|звезды|звезда|★)",
        ]

        for pattern in patterns:
            match = re.search(pattern, source, flags=re.IGNORECASE)
            if match:
                return int(match.group(1))

        return None

    def _extract_date(self, row: dict, raw_text: str) -> Optional[datetime]:
        raw_date = (
            row.get("datetime")
            or row.get("date")
            or row.get("created_at")
            or row.get("created_at_origin")
            or ""
        )

        raw_date = str(raw_date).strip()

        if raw_date:
            for fmt in (
                "%Y-%m-%d",
                "%Y-%m-%d %H:%M:%S",
                "%d.%m.%Y",
                "%d/%m/%Y",
            ):
                try:
                    return datetime.strptime(raw_date, fmt)
                except ValueError:
                    pass

            try:
                return datetime.fromisoformat(raw_date)
            except ValueError:
                pass

        source = " ".join(str(v) for v in row.values() if v)
        source += " " + raw_text

        ru_months = {
            "января": 1,
            "февраля": 2,
            "марта": 3,
            "апреля": 4,
            "мая": 5,
            "июня": 6,
            "июля": 7,
            "августа": 8,
            "сентября": 9,
            "октября": 10,
            "ноября": 11,
            "декабря": 12,
        }

        match = re.search(
            r"\b(\d{1,2})\s+"
            r"(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)"
            r"(?:\s+(\d{4}))?\b",
            source,
            flags=re.IGNORECASE,
        )

        if match:
            day = int(match.group(1))
            month = ru_months[match.group(2).lower()]
            year = int(match.group(3)) if match.group(3) else datetime.utcnow().year

            try:
                return datetime(year, month, day)
            except ValueError:
                pass

        return datetime.utcnow()