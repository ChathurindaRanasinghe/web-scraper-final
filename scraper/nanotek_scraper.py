from pprint import pprint
from products.cpu import get_cpu_specs
from products.power_supply import get_power_supply_specs
from products.storage import get_storage_specs
from web.web_page import WebPage
from url_lists.nanotek import BASE_URL_NANOTEK
from bs4 import BeautifulSoup
from products.product import find_product_index
import pandas as pd
import lxml, cchardet


def get_category_nanotek(url: str) -> str:
    category = url.replace(BASE_URL_NANOTEK, '').split("?")[0]
    if category == 'storage':
        return 'storage'
    elif category == 'processors':
        return 'cpu'
    elif category == "power-supply":
        return 'power-supply'
    # elif category == "graphic-cards":
    #     return "gpu"
    

def nanotek_scraper(web_page: WebPage, products: dict) -> None:
    category = get_category_nanotek(url=web_page.url)
    df = None
    name_arr = None
    capcity_arr = None
    #count = 0
    # print(category)
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
    # elif category == "gpu":
    #     df = pd.read_csv("base_data/gpu_base_data.csv")
    #     name_arr = (df['Name1']).to_numpy()
    #     capcity_arr = (df['Memory']).to_numpy()
    

    soup = BeautifulSoup(web_page.page, 'lxml')
    elements = soup.find_all("li", {"class": "ty-catPage-productListItem"})
    for  element in elements:
        
        product_name = element.find(
            "div", {"class": "ty-productBlock-title"}).text.lower().strip()
        product_price = int(element.find("h2", {"class": "ty-productBlock-price-retail"}).text.replace(",", ""))
        product_link = element.find("a").get("href")
        product_availability = False if element.find(
            "div", {"class": "ty-productBlock-specialMsg"}).text.strip().lower() == "out of stock" else True

        index = None
        highest_ratio = 0
        if category == "storage":
            index, highest_ratio = find_product_index(category, product_name,df,name_arr,capcity_arr)
        elif category == "cpu":
            index, highest_ratio = find_product_index(category=category, name = product_name,df = df,name_arr = name_arr)
        elif category == "power-supply":
            index, highest_ratio = find_product_index(category, product_name,df,name_arr,capcity_arr)
        # elif category == "gpu":
        #     index, highest_ratio = find_product_index(category, product_name,df,name_arr,capcity_arr)
        
        if highest_ratio >= 90 and index != None:
            #count+=1
            # print(f"{products[category][index].name} - {product_name} - {highest_ratio}")
            products[category][index].shops['nanotek'] = product_name
            products[category][index].links['nanotek'] = product_link
            products[category][index].availability['nanotek'] = product_availability
            products[category][index].prices['nanotek'] = product_price
            
            if category == 'storage':
                products[category][index].specs = get_storage_specs(index,df)
            elif category == 'cpu':
                products[category][index].specs = get_cpu_specs(index,df)
            elif category == 'power-supply':
                products[category][index].specs = get_power_supply_specs(index,df)
                # print(products[category][index].specs)

    #print(f"{count}/{len(elements)}")
