from web.web_page import WebPage
from url_lists.nanotek import BASE_URL_NANOTEK
from url_lists.gamestreet import BASE_URL_GAMESTREET
from url_lists.tech_zone import BASE_URL_TECH_ZONE
from .nanotek_scraper import nanotek_scraper
from .gamestreet_scraper import gamestreet_scraper
from .tech_zone_scraper import tech_zone_scraper


def main_scraper(web_page: WebPage, products: dict) -> None:
    if BASE_URL_NANOTEK in web_page.url:
        nanotek_scraper(web_page, products)
    elif BASE_URL_GAMESTREET in web_page.url:
        gamestreet_scraper(web_page, products)
    elif BASE_URL_TECH_ZONE in web_page.url:
        tech_zone_scraper(web_page,products)

