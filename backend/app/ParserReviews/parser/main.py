import csv
import datetime as dt
import logging
<<<<<<< HEAD
import re
import time
from pathlib import Path
=======
import os
import re
import time
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1

from selenium.webdriver import Firefox
from selenium.webdriver.remote.webelement import WebElement
from tqdm import tqdm

<<<<<<< HEAD
from . import selenium_helper as sh
from .classes import Review

logger: logging.Logger = logging.getLogger(__name__)


def save_csv(data, filepath):
    """Save parsed reviews to CSV file."""
=======
from backend.app.ParserReviews.parser import selenium_helper as sh
from backend.app.ParserReviews.parser.classes import Review

logger: logging.Logger = logging.getLogger(__name__)

from .db import get_db
from .models import Review
from sqlalchemy.exc import IntegrityError

def save_review_to_db(review_data: dict):
    """Сохраняет отзыв в БД, если его ещё нет."""
    db = next(get_db())
    try:
        # Проверяем, есть ли уже такой external_id
        existing = db.query(Review).filter(Review.external_id == review_data["external_id"]).first()
        if existing:
            return
        db_review = Review(**review_data)
        db.add(db_review)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # возможно дубликат, игнорируем
    finally:
        db.close()

def save_csv(data, filepath):
    """Save data to CSV file"""
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
    if not data:
        logger.warning("No data to save")
        return

<<<<<<< HEAD
=======
    
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
    flattened_data = []
    for item in data:
        flat_item = {}
        for key, value in item.items():
            if isinstance(value, dict):
<<<<<<< HEAD
                for nested_key, nested_value in value.items():
                    flat_item[f"{key}_{nested_key}"] = nested_value
            elif isinstance(value, list):
                flat_item[key] = ", ".join(map(str, value)) if value else ""
            else:
                flat_item[key] = value if value is not None else ""
        flattened_data.append(flat_item)

=======
                
                for nested_key, nested_value in value.items():
                    flat_item[f"{key}_{nested_key}"] = nested_value
            elif isinstance(value, list):
                
                flat_item[key] = ', '.join(map(str, value)) if value else ''
            else:
                flat_item[key] = value if value is not None else ''
        flattened_data.append(flat_item)

    # Get all possible field names
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
    fieldnames = set()
    for item in flattened_data:
        fieldnames.update(item.keys())
    fieldnames = sorted(list(fieldnames))

<<<<<<< HEAD
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with filepath.open("w", encoding="utf-8-sig", newline="") as csv_file:
=======
    # Write to CSV
    with open(filepath, 'w', encoding='utf-8-sig', newline='') as csv_file:
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flattened_data)

<<<<<<< HEAD
    logger.info(f"Saved {filepath}")


def save_json(data, filepath):
    import json

    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with filepath.open("w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
    logger.info(f"Saved {filepath}")


def mode_script_content(driver: Firefox, filepath):
    import json

    script_element = driver.find_element(by="xpath", value='//script[@class="state-view"]')
    script_content = script_element.get_attribute("innerHTML")
    save_json(json.loads(script_content), filepath)
=======
    logger.info(f'Saved {filepath}')


def save_json(data, filepath):
    """Keep original JSON save function if needed"""
    import json
    with open(filepath, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
    logger.info(f'Saved {filepath}')


def mode_script_content(driver: Firefox, filepath):
    """Original function kept for JSON mode"""
    import json
    script_element = driver.find_element(by='xpath', value='//script[@class="state-view"]')
    script_content = script_element.get_attribute("innerHTML")
    save_json(
        json.loads(script_content),
        filepath,
    )
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1


def mode_reviews(driver: Firefox, filepath):
    for i in reversed(range(1, 5 + 1)):
        logger.info(f"{i}...")
        time.sleep(1)
<<<<<<< HEAD

    total_reviews_elem: WebElement = sh.wait_element_by_xpath(
=======
    total_reviews: WebElement = sh.wait_element_by_xpath(
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
        driver=driver,
        xpath='//*[@class="card-section-header__title _wide"]',
    )

<<<<<<< HEAD
    total_reviews = int(re.sub(pattern=r"\D", repl="", string=total_reviews_elem.text))
    data = []

    for i in tqdm(range(1, total_reviews + 1), desc="Loading all reviews on the page"):
        review_elem = sh.wait_element_by_xpath(
            xpath=f'(//*[@class="business-review-view__info"])[{i}]',
            driver=driver,
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", review_elem)
=======
    total_reviews: int = int(re.sub(pattern=r'\D',
                                    repl='',
                                    string=total_reviews.text
                                    ))
    data = []
    for i in tqdm(range(1, total_reviews + 1), desc="Loading all reviews on the page"):
        review_elem = sh.wait_element_by_xpath(
            xpath=f'''(//*[@class="business-review-view__info"])[{i}]''',
            driver=driver
        )

        driver.execute_script(
            "arguments[0].scrollIntoView(true);", review_elem
        )
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1

        new_review = Review()
        new_review.parse_base_information(review_elem=review_elem)
        new_review.try_add_response(review_elem=review_elem, driver=driver)

        data.append(new_review.__dict__)

<<<<<<< HEAD
    save_csv(data, filepath)


MODE_DICT = {
    "reviews": mode_reviews,
    "experimental": mode_script_content,
}


def get_organization_reviews(
    driver: Firefox,
    mode: str,
    implicitly_wait: int = 0,
    org_id: int | str = 1124715036,
    output_format: str = "csv",
    output_dir: str | Path | None = None,
) -> str:
    organization_url = f"https://yandex.ru/maps/org/yandeks/{org_id}/reviews/"
    logger.info(f"Start {organization_url=} {implicitly_wait=}")
    driver.implicitly_wait(implicitly_wait)

    file_dttm = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d_%H-%M-%S")
    extension = "csv" if output_format == "csv" else "json"

    if output_dir is None:
        output_dir = Path(__file__).resolve().parents[1] / extension
    else:
        output_dir = Path(output_dir)

    target_filename = f"{org_id}_{mode}_{file_dttm}.{extension}"
    filepath = output_dir / target_filename

    driver.get(organization_url)
    MODE_DICT[mode](driver=driver, filepath=filepath)

    return str(filepath)


if __name__ == "__main__":
=======
        # Сохраняем в БД
        review_dict = new_review.__dict__.copy()
        review_dict["external_id"] = review_dict.get("selenium_id", f"unknown_{i}")
        save_review_to_db(review_dict)
    save_csv(data, filepath)  


MODE_DICT = {
    'reviews': mode_reviews,
    'experimental': mode_script_content,
}


def get_organization_reviews(driver: Firefox,
                             mode: str,
                             implicitly_wait: int = 0,
                             org_id: int = 1124715036,
                             output_format: str = 'csv'): 
    organization_url = f"https://yandex.ru/maps/org/yandeks/{org_id}/reviews/"
    logger.info(f'Start {organization_url=} {implicitly_wait=}')
    driver.implicitly_wait(implicitly_wait)
    file_dttm: str = dt.datetime.now(dt.UTC).strftime('%Y-%m-%d %H-%M-%S')

    
    extension = 'csv' if output_format == 'csv' else 'json'
    target_filename = f'{org_id}_{mode}_{file_dttm}.{extension}'
    filepath = os.path.join(os.getcwd(), extension, target_filename)

    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    driver.get(organization_url)

    MODE_DICT[mode](driver=driver, filepath=filepath)


if __name__ == '__main__':
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
    pass
