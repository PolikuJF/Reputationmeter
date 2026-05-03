import csv
import datetime as dt
import logging
import os
import re
import time

from selenium.webdriver import Firefox
from selenium.webdriver.remote.webelement import WebElement
from tqdm import tqdm

from parser import selenium_helper as sh
from parser.classes import Review

logger: logging.Logger = logging.getLogger(__name__)


def save_csv(data, filepath):
    """Save data to CSV file"""
    if not data:
        logger.warning("No data to save")
        return

    
    flattened_data = []
    for item in data:
        flat_item = {}
        for key, value in item.items():
            if isinstance(value, dict):
                
                for nested_key, nested_value in value.items():
                    flat_item[f"{key}_{nested_key}"] = nested_value
            elif isinstance(value, list):
                
                flat_item[key] = ', '.join(map(str, value)) if value else ''
            else:
                flat_item[key] = value if value is not None else ''
        flattened_data.append(flat_item)

    # Get all possible field names
    fieldnames = set()
    for item in flattened_data:
        fieldnames.update(item.keys())
    fieldnames = sorted(list(fieldnames))

    # Write to CSV
    with open(filepath, 'w', encoding='utf-8-sig', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flattened_data)

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


def mode_reviews(driver: Firefox, filepath):
    for i in reversed(range(1, 5 + 1)):
        logger.info(f"{i}...")
        time.sleep(1)
    total_reviews: WebElement = sh.wait_element_by_xpath(
        driver=driver,
        xpath='//*[@class="card-section-header__title _wide"]',
    )

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

        new_review = Review()
        new_review.parse_base_information(review_elem=review_elem)
        new_review.try_add_response(review_elem=review_elem, driver=driver)

        data.append(new_review.__dict__)

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
    pass
