import csv
import logging
from selenium.common.exceptions import (
    NoSuchElementException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

logger = logging.getLogger(__name__)


def try_get_child_elem_by_xpath(
        parent_element: WebElement, value: str
) -> WebElement or None:
    found_elem = parent_element.find_elements(
        by=By.XPATH, value=value
    )
    logger.debug(
        f"{len(found_elem)=} {value} {parent_element.get_attribute('outerHTML')=}"
    )
    return found_elem[0] if found_elem else None


def try_found_elem_if_exist_return_attr(
        parent_element: WebElement or None,
        attribute: str,
) -> str or None:
    if parent_element:  # is WebElement
        return parent_element.get_attribute(attribute)


def try_found_elem_if_exist_return_text(
        parent_element: WebElement or None
) -> str or None:
    if parent_element:
        return parent_element.text


def get_dict_from_meta(
        parent_element: WebElement, value: str
) -> dict:
    return {
        meta.get_attribute("itemprop"): [
            meta.get_attribute("content"),
            meta.text,
        ]
        for meta in parent_element.find_elements(
            By.XPATH, value
        )
    }


class Review:
    """class for reviews"""

    def __repr__(self):
        return repr(self.__dict__)

    def __init__(self, **kwargs):

        self.response_text = None
        self.response_datetime = None
        self.is_a_response = True
        self.dislike = None
        self.like = None
        self.review_text = None
        self.author_url = None
        self.author = None
        self.review_rating = None
        self.datetime = None
        self.selenium_id = None

        for key, value in kwargs.items():
            setattr(self, key, value)

    def parse_base_information(
            self, review_elem: WebElement
    ):
        self.selenium_id = review_elem.id
        self.datetime = get_dict_from_meta(
            review_elem,
            './/*[@class="business-review-view__date"]//*',
        )
        self.review_rating = get_dict_from_meta(
            review_elem,
            './/*[@itemtype="http://schema.org/Rating"]//*',
        )
        self.author = get_dict_from_meta(
            review_elem,
            './/*[@itemtype="http://schema.org/Person"]//*',
        )
        self.author_url = (
            try_found_elem_if_exist_return_attr(
                review_elem,
                "href",
            )
        )
        self.review_text = try_found_elem_if_exist_return_text(
            review_elem,
        )
        self.like = try_found_elem_if_exist_return_text(
            review_elem,
        )
        self.dislike = try_found_elem_if_exist_return_text(
            review_elem,
        )

    def try_add_response(self, review_elem, driver):
        self.is_a_response = False
        try:
            elem_comment_expand = review_elem.find_element(
                by=By.XPATH,
                value='.//*[@class="business-review-view__comment-expand"]',
            )
            driver.execute_script(
                "arguments[0].scrollIntoView(true);",
                elem_comment_expand,
            )
            driver.execute_script(
                "arguments[0].click();", elem_comment_expand
            )
            self.response_datetime = try_found_elem_if_exist_return_text(
                review_elem,
            )
            self.response_text = try_found_elem_if_exist_return_text(
                review_elem,
            )
        except NoSuchElementException:
            pass

    @staticmethod
    def save_to_csv(reviews_list, filepath):
        """
        Сохраняет список объектов Review в CSV файл.
        Словари и списки преобразуются в строки для совместимости с CSV.
        """
        if not reviews_list:
            logger.warning("No reviews to save")
            return

        
        fieldnames = set()
        for review in reviews_list:
            if isinstance(review, Review):
                fieldnames.update(review.__dict__.keys())
            else:
                fieldnames.update(review.keys())
        fieldnames = sorted(list(fieldnames))

        
        with open(filepath, 'w', encoding='utf-8-sig', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for review in reviews_list:
                
                if isinstance(review, Review):
                    review_dict = review.__dict__
                else:
                    review_dict = review

                
                row = {}
                for key, value in review_dict.items():
                    if isinstance(value, dict):
                        row[key] = '; '.join(
                            [f"{k}: {v}" for k, v in value.items() if v]
                        ) if value else ''
                    elif isinstance(value, list):
                        row[key] = ', '.join(
                            [str(item) for item in value if item]
                        ) if value else ''
                    elif value is None:
                        row[key] = ''
                    else:
                        row[key] = value

                writer.writerow(row)

        logger.info(f'Saved {len(reviews_list)} reviews to {filepath}')


if __name__ == '__main__':
    pass
