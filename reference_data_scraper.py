import asyncio
from pprint import pprint
import re
from time import time
import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
from typing import List
import lxml
import cchardet
import uvloop

pages = []
cpu_pages = []

timeout = None
wait = None
splash = None


async def download_link_and_scrape(url: str, session: ClientSession, cpu: bool = False) -> None:
    async with session.get(url) as response:
        # print(url)
        result = await response.text()
        print(response.status)
        if response.status == 200:
            if cpu:
                cpu_pages.append(result)
            else:
                pages.append(result)
        return None


async def download_all(urls: list, cpu: bool = False) -> None:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(
                download_link_and_scrape(url=url, session=session, cpu=cpu))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


def extract_details_cpu(pages: List[str]) -> List[str]:
    cpu_links = []
    # print("inside extract details cpu")
    cpu_count = 0
    for page in pages:
        only_items = SoupStrainer("div", attrs={"class": "chip-list"})
        soup = BeautifulSoup(page, 'lxml', parse_only=only_items)
        elements = soup.find_all("div", {"class": "item mb2"})
        print(len(elements))
        #elements = soup.find("div",{"class": "chip-list"}).find_all("div",{"class":"item mb2"})
        cpu_count += len(elements)
        for element in elements:
            url = "https://www.hardwaredb.net" + \
                element.find("a", {"class": "text-medium"}).get("href")
            if splash:
                url = f"http://localhost:8050/render.html?url={url}&wait={wait}&timeout={timeout}"
            # print(url)
            cpu_links.append(url)
            # print(element.find("a",{"class":"text-medium"}).get_text())
    return cpu_links


def extract_details_cpu_page(page) -> dict:
    cpu = {}
    soup = BeautifulSoup(page, 'lxml')
    #print(soup.find('div',{'class':'sm-col12 md-col10 md-pl3'}))
    cpu['name'] = soup.find('h1', {'class': 'mb'}).get_text(
    ).lower().replace(' benchmark', '')
    cpu['overall-benchmark-score'] = re.findall(
        r'[0-9]+', soup.find('div', {'class': 'score mb'}).text)[0]
    cpu['gaming-benchmark-score'] = re.findall(r'[0-9]+', soup.find('table', {
                                               'class': 'benchmark-score-detail mb2'}).find('td', {'class': 'value'}).text)[0]
    cpu['multitasking-benchmark-score'] = re.findall(r'[0-9]+', soup.find(
        'table', {'class': 'benchmark-score-detail mb2'}).find_all('td', {'class': 'value'})[1].text)[0]
    cpu['multitasking-benchmark-score'] = re.findall(r'[0-9]+', soup.find(
        'table', {'class': 'benchmark-score-detail mb2'}).find_all('td', {'class': 'value'})[2].text)[0]
    # pprint(cpu)


def scrape_and_save_reference() -> None:
    cpu_urls: List[str] = []
    if splash:
        cpu_urls = [
            f"http://localhost:8050/render.html?url=https://www.hardwaredb.net/cpu-database/page-{i}&wait={wait}&timeout={timeout}" for i in range(0, 50)]
    else:
        cpu_urls = [
            f"https://www.hardwaredb.net/cpu-database/page-{i}" for i in range(0, 50)]

    uvloop.install()
    asyncio.run(download_all(urls=cpu_urls))
    # pprint(pages[0])
    cpu_spec_urls = extract_details_cpu(pages)
    #cpu_spec_urls = cpu_spec_urls[:1]
    #print(len(cpu_spec_urls))
    asyncio.run(download_all(urls=cpu_spec_urls, cpu=True))

    # with open('test.html','w') as f:
    #     f.write(cpu_pages[0])
    # pprint(cpu_pages[0])
    for page in cpu_pages:
        extract_details_cpu_page(page)


if __name__ == "__main__":
    import cProfile
    import pstats

    splash = False
    timeout = 50
    wait = 2

    count = 0
    scrape_and_save_reference()
    # with cProfile.Profile() as pr:
    #     scrape_and_save_reference()
    # #print(len(cpu_pages))()

    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # # # stats.print_stats()
    # stats.dump_stats(filename="profile.prof")
    # print(count)
    
    print(f"pages-length={len(pages)}")
    print(f"cpu-pages-length={len(cpu_pages)}")
