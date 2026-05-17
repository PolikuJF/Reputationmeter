import logging
import re
import time
from datetime import datetime
from pathlib import Path

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models
from app.nlp.mock_nlp import analyze_sentiment, extract_topics
from app.parsers.yandex_csv_parser import YandexCsvParser
from app.ParserReviews.parser.log import configure_logging
from app.ParserReviews.parser.main import get_organization_reviews
from app.ParserReviews.parser.selenium_helper import make_driver

logger = logging.getLogger(__name__)


def extract_yandex_org_id(platform_url: str | None) -> str | None:
    """Extract Yandex organization id from links like /org/name/1124715036/reviews/."""
    if not platform_url:
        return None

    patterns = [
        r"/org/[^/]+/(\d+)",
        r"/org/(\d+)",
        r"[?&]oid=(\d+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, platform_url)
        if match:
            return match.group(1)

    numbers = re.findall(r"\d{6,}", platform_url)
    return numbers[-1] if numbers else None


def run_live_yandex_parser(establishment: models.Establishment) -> str | None:
    """Run existing Selenium Yandex parser and return generated CSV path."""
    org_id = extract_yandex_org_id(establishment.platform_url)

    if not org_id:
        logger.warning("Could not extract Yandex org_id from URL: %s", establishment.platform_url)
        return None

    configure_logging(debug=False)

    output_dir = Path("app/ParserReviews/csv")
    output_dir.mkdir(parents=True, exist_ok=True)

    last_error = None

    for attempt in range(1, 4):
        try:
            with make_driver(debug=False) as driver:
                return get_organization_reviews(
                    org_id=org_id,
                    driver=driver,
                    implicitly_wait=1,
                    mode="reviews",
                    output_format="csv",
                    output_dir=output_dir,
                )
        except Exception as exc:
            last_error = exc
            logger.exception("Yandex parser attempt %s failed", attempt)
            time.sleep(2 ** attempt)

    raise RuntimeError(f"Yandex parser failed after 3 attempts: {last_error}")


def run_parsing_for_establishment(db: Session, establishment: models.Establishment) -> dict:
    log = models.ParsingLog(
        establishment_id=establishment.id,
        started_at=datetime.utcnow(),
        status="running",
        reviews_fetched=0,
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    try:
        csv_path = run_live_yandex_parser(establishment)

        if csv_path:
            parser = YandexCsvParser(csv_path=csv_path)
            source = "live_yandex"
        else:
            parser = YandexCsvParser()
            source = "fallback_csv"

        parsed_reviews = parser.parse_reviews(establishment)

        saved_count = 0
        skipped_count = 0
        seen_external_ids = set()

        for parsed in parsed_reviews:
            if not parsed.external_id:
                skipped_count += 1
                continue

            if parsed.external_id in seen_external_ids:
                skipped_count += 1
                continue

            seen_external_ids.add(parsed.external_id)

            if not parsed.text or not parsed.text.strip():
                skipped_count += 1
                continue

            exists = db.query(models.Review).filter(
                models.Review.external_id == parsed.external_id
            ).first()

            if exists:
                skipped_count += 1
                continue

            sentiment = analyze_sentiment(parsed.text or "")
            topics = extract_topics(parsed.text or "")

            review = models.Review(
                establishment_id=establishment.id,
                external_id=parsed.external_id,
                author_name=parsed.author_name,
                rating=parsed.rating,
                text=parsed.text,
                created_at_origin=parsed.created_at_origin or datetime.utcnow(),
                sentiment=sentiment,
                topics=",".join(topics),
                is_processed=True,
                status="new",
            )

            try:
                db.add(review)
                db.flush()
                saved_count += 1
            except IntegrityError:
                db.rollback()
                skipped_count += 1
                continue

        establishment.last_parsed_at = datetime.utcnow()

        log.status = "success"
        log.finished_at = datetime.utcnow()
        log.reviews_fetched = saved_count

        db.commit()

        return {
            "status": "success",
            "source": source,
            "establishment_id": establishment.id,
            "saved_reviews": saved_count,
            "skipped_reviews": skipped_count,
        }

    except Exception as exc:
        db.rollback()

        log.status = "failed"
        log.finished_at = datetime.utcnow()
        log.error_message = str(exc)

        db.add(log)
        db.commit()

        raise
