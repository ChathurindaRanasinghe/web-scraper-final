from pprint import pprint
from typing import Dict, List

from bs4 import BeautifulSoup
from web.web_page import WebPage
import lxml, cchardet

BASE_URL_GOOGLE_SEARCH = "https://www.google.lk/search?q="

shops: List[str] = ["gamestreet","techzone","redtech","redline-technologies","nanotek"] # ,

urls: List[str] = [BASE_URL_GOOGLE_SEARCH + shop for shop in shops]

# def get_pages() -> List[WebPage]:
#     pages = []
#     for url in urls:
#         pages.append(WebPage(url,requests.get(url).text))
#     return pages

# def scrape_shop_data() -> Dict:
#     pages:List[WebPage] = get_pages()
#     for web_page in pages:
#         soup = BeautifulSoup(web_page.page,'lxml')
#         element = soup.find("div",{"class":"osrp-blk"}).find_next("div",{"class":"QqG1Sd"})
#         pprint(element)