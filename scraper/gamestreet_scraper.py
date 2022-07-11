from pprint import pprint
from products.cpu import get_cpu_specs
from products.power_supply import get_power_supply_specs
from products.product import find_product_index
from products.storage import get_storage_specs
from web.web_page import WebPage
from url_lists.gamestreet import BASE_URL_GAMESTREET, GAMESTREET_WEBSITE
from bs4 import BeautifulSoup
import pandas as pd
import re
import lxml, cchardet

def get_category_from_url(url: str) -> str:
    category = url.replace(BASE_URL_GAMESTREET,'')
    if category == "=Mg==&scat=MTM=" or category == "=Mg==&scat=MTE=":
        return "storage"
    elif category == "=Mg==&scat=MQ==":
        return "cpu"
    elif category == "=Mg==&scat=NQ==":
        return "power-supply"
    elif category == "=Mg==&scat=Mg==":
        return 'motherboard'


def gamestreet_scraper(web_page: WebPage, products: dict) -> None:
    category = get_category_from_url(url=web_page.url)
    #pprint(web_page.page)
    count = 0
    df = None
    name_arr = None
    capcity_arr = None
    if category == "storage":
        df = pd.read_csv("base_data/storage_base_data.csv")
        name_arr = (df['Name1']).to_numpy()
        capcity_arr = (df['Capacity']).to_numpy()
    elif category == "cpu":
       df = pd.read_csv("base_data/cpu_base_data.csv")
       name_arr = (df['Name1']).to_numpy()
    elif category == "power-supply":
        df = pd.read_csv("base_data/power_supply_base_data.csv")
        name_arr = (df['Name1']).to_numpy()
        capcity_arr = (df['Wattage']).to_numpy()
    elif category == 'motherboard':
        df = pd.read_csv("base_data/motherboard_base_data.csv")
        name_arr = (df['Name1']).to_numpy()

    soup = BeautifulSoup(web_page.page, 'lxml')
    elements = soup.find_all('div', {'class': 'col-sm-4 MrgTp35'})
    for  element in elements:
        product_name = element.find('div', {'class': 'product_title'}).find('a').get_text().lower()
        print(product_name)
        try:
            product_price = float(re.sub(r'Rs\.|,', '', element.find('span', {'class': 'redPrice'}).get_text()))
        except AttributeError:
            continue
        product_link = GAMESTREET_WEBSITE + element.find('div', {'class': 'product_title'}).find('a').get('href')
        # TODO: scrape inside product link, get specs
        #stock_status = element.find('dl',{'class':'dl-horizontal ProInfo'}).find_all('dd')
        product_availability = True#(lambda: False, lambda: True)['in' in stock_status[3].get_text().lower()]()

        index = None
        highest_ratio = 0
        if category == "storage":
            index, highest_ratio = find_product_index(category, product_name,df,name_arr,capcity_arr)
        elif category == "cpu":
            index, highest_ratio = find_product_index(category=category, name = product_name,df = df,name_arr = name_arr)
        elif category == "power-supply":
            index, highest_ratio = find_product_index(category, product_name,df,name_arr,capcity_arr)
        elif category == "motherboard":
            index, highest_ratio = find_product_index(category=category, name = product_name,df = df,name_arr = name_arr)
            
        if highest_ratio >= 90:
            count += 1
            # print(f'{highest_ratio} - {product_name} - {products[category][index].name}')
            products[category][index].shops['gamestreet'] = product_name
            products[category][index].links['gamestreet'] = product_link
            products[category][index].availability['gamestreet'] = product_availability
            products[category][index].prices['gamestreet'] = product_price

            if category == 'storage':
                products[category][index].specs = get_storage_specs(index,df)
            elif category == 'cpu':
                products[category][index].specs = get_cpu_specs(index,df)
            elif category == 'power-supply':
                products[category][index].specs = get_power_supply_specs(index,df)

    print(f"{count}/{len(elements)}")
