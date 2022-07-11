import asyncio
from pprint import pprint
import aiohttp
from aiohttp import ClientSession
from attr import attrs
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
from typing import List
import lxml, cchardet
import cProfile,pstats
import uvloop

pages = []

cpu_pages = []

async def download_link_and_scrape(url: str, session: ClientSession, cpu:bool = False) -> None:
    async with session.get(url) as response:
        # print(url)
        result = await response.text()
        if response.status == 200:
            if cpu:
                cpu_pages.append(result)
            else:
                pages.append(result)


async def download_all(urls: list, cpu:bool = False) -> None:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(
                download_link_and_scrape(url=url, session=session,cpu=cpu))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


def extract_details_cpu(pages:List[str]) -> List[str]:
    cpu_links = []
    cpu_count = 0
    for page in pages:
        only_items = SoupStrainer("div",attrs={"class": "chip-list"})
        soup = BeautifulSoup(page,'lxml',parse_only=only_items)
        elements = soup.find_all("div",{"class":"item mb2"})
        #elements = soup.find("div",{"class": "chip-list"}).find_all("div",{"class":"item mb2"})
        cpu_count += len(elements)
        for element in elements:
            cpu_links.append("https://www.hardwaredb.net" + element.find("a",{"class":"text-medium"}).get("href"))
            #print(element.find("a",{"class":"text-medium"}).get_text())
    return cpu_links


def extract_details_cpu_page(page) -> dict:
    cpu = {}
    soup = BeautifulSoup(page,'lxml')
    print(soup.find('div',{'class':'sm-col12 md-col10 md-pl3'}))
    #cpu['name'] = soup.find('h1',{'class':'mb'}).get_text().lower().replace(' benchmark','')
    #cpu['overall-benchmark-score'] = soup.find('h1',{'class':'score mb'}).get_text()
    #cpu['gaming-benchmark-score'] = soup.find
    print(cpu)


def scrape_and_save_reference() -> None:
    cpu_urls: List[str] = [f"https://www.hardwaredb.net/cpu-database/page-{i}?sort=0" for i in range(0,50)]
    uvloop.install()
    asyncio.run(download_all(urls=cpu_urls))
    cpu_spec_urls = extract_details_cpu(pages)
        
    # asyncio.run(download_all(urls=cpu_spec_urls,cpu=True))
    # pprint(pages[0])
    # extract_details_cpu_page(pages[0])


if __name__ == "__main__":
    
    with cProfile.Profile() as pr:
        scrape_and_save_reference()
    #print(len(cpu_pages))()
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # # stats.print_stats()
    stats.dump_stats(filename="profile.prof")
