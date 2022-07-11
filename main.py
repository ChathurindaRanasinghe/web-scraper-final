import asyncio
from pprint import pprint
import time
import aiohttp
from aiohttp.client import ClientSession
import uvloop
from url_lists.gamestreet import generate_url_list_gamestreet
from url_lists.tech_zone import generate_url_list_tech_zone
from web.web_page import WebPage
from products.product import init_products
from url_lists.nanotek import generate_url_list_nanotek
from scraper.main_scraper import main_scraper
import cProfile
import pstats
import numpy as np
from database import connect_database, save_data

pages = []

async def download_link_and_scrape(url: str, session: ClientSession) -> None:
    async with session.get(url) as response:
        result = await response.text()
        # print(response.status)
        if response.status == 200:
            pages.append(WebPage(url=url, page=result))


async def download_all(urls: list) -> None:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(
                download_link_and_scrape(url=url, session=session))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)

def scrape_and_save():
    url_list: list =  generate_url_list_nanotek()  + generate_url_list_tech_zone() + generate_url_list_gamestreet() #
    uvloop.install()
    asyncio.run(download_all(urls=url_list))
    product_list: dict = init_products()
    for page in pages:
        main_scraper(web_page=page, products=product_list)
    #save_data(products=product_list,local_db=True)
    # count = 0
    # for product in product_list['storage'] + product_list['cpu'] + product_list['power-supply']:
    #     if bool(product.shops):
    #         count += 1
    # print(count)

if __name__ == "__main__":
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #asyncio.run(download_all(urls=shop_urls))
    # scrape_shop_data()
    
    # # start = time.perf_counter()
    # scrape_and_save()
    with cProfile.Profile() as pr:
        scrape_and_save()
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # # stats.print_stats()
    stats.dump_stats(filename="profile.prof")
    
    # elapsed = time.perf_counter() - start
    # print(f"Requests ==> time taken: {elapsed:.2f}s")
    
    # 

    # start = time.perf_counter()
    # scrape_and_save()
    # elapsed = time.perf_counter() - start
    # print(f"Scraping & Saving ==> time taken: {elapsed:.2f}s")

    # with cProfile.Profile() as pr:
    #     scrape_and_save()

    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # # stats.print_stats()
    # stats.dump_stats(filename="profile.prof")

    #elapsed = time.perf_counter() - start

    #print(f"Requests ==>time taken: {elapsed:.2f}s")
    

