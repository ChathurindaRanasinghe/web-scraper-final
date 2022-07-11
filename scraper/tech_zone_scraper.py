from products.cpu import get_cpu_specs
from products.power_supply import get_power_supply_specs
from products.storage import get_storage_specs
from web.web_page import WebPage
from url_lists.tech_zone import BASE_URL_TECH_ZONE
from bs4 import BeautifulSoup
from products.product import find_product_index
import pandas as pd
import lxml, cchardet


def get_category_tech_zone(url: str) -> str:
    category = url.replace(BASE_URL_TECH_ZONE, '').split("/")[0]
    if category == 'storage':
        return 'storage'
    elif category == 'processor':
        return 'cpu'
    elif category == 'power-supply':
        return 'power-supply'
    elif category == 'motherboard':
        return 'motherboard'


def tech_zone_scraper(web_page: WebPage, products: dict) -> None:
    category = get_category_tech_zone(url=web_page.url)
    df = None
    name_arr = None
    capcity_arr = None
    count = 0
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
    elif category == "motherboard":
        df = pd.read_csv("base_data/motherboard_base_data.csv")
        name_arr = (df['Name1']).to_numpy() 

    soup = BeautifulSoup(web_page.page, 'lxml')
    elements = soup.find_all('div',{'class':'product-inner product-item__inner'})
    
    for element in elements:
        product_name = element.find('h2',{'class':'woocommerce-loop-product__title'}).text.lower().strip()
        product_price = float(element.find('span',{'class':'woocommerce-Price-amount amount'}).text.replace("රු",'').replace(',',''))
        product_link = element.find('a',{'class':'woocommerce-LoopProduct-link woocommerce-loop-product__link'}).get('href')
        product_availability = None
    
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
        
        if highest_ratio >= 90 and index != None:
            count +=1
            # print(f'{product_name} - {products[category][index].name} - {highest_ratio}')
            products[category][index].shops['tech-zone'] = product_name
            products[category][index].links['tech-zone'] = product_link
            products[category][index].availability['tech-zone'] = product_availability
            products[category][index].prices['tech-zone'] = product_price

            if category == 'storage':
                products[category][index].specs = get_storage_specs(index,df)
            elif category == 'cpu':
                products[category][index].specs = get_cpu_specs(index,df)
            elif category == 'power-supply':
                products[category][index].specs = get_power_supply_specs(index,df)
    print(f"{count}/{len(elements)}")