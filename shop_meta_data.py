import asyncio
from pprint import pprint
from typing import Dict, List
from aiohttp import ClientSession
import aiohttp

from bs4 import BeautifulSoup
from web.web_page import WebPage
import lxml, cchardet

BASE_URL_GOOGLE_SEARCH = "https://www.google.lk/search?q="
shops: List[str] = ["gamestreet","techzone","redtech","redline-technologies","nanotek"] # ,

wait_time = 2

urls: List[str] = [ f"http://localhost:8050/render.html?url={BASE_URL_GOOGLE_SEARCH + shop}&wait={wait_time}" for shop in shops]


pages = []

async def download_link_and_scrape(url: str, session: ClientSession) -> None:
    async with session.get(url) as response:
        result = await response.text()
        # print(response.status)
        pages.append(result)


async def download_all(urls: list) -> None:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(
                download_link_and_scrape(url=url, session=session))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)





def scrape_shop_data() -> Dict:
    for web_page in pages:
        soup = BeautifulSoup(web_page,'lxml')
        website = soup.find("div",{"class":"osrp-blk"}).find("div",{"class":"QqG1Sd"}).find('a').get("href")
        review_score = soup.find('span',{'class':'Aq14fc'}).text
        pprint(review_score)

if __name__ == '__main__':
    # need splash
    asyncio.run(download_all(urls))
    scrape_shop_data()