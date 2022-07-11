from typing import List


BASE_URL_TECH_ZONE = "https://techzone.lk/product-category/computer-components/"

CATEGORIES_TECHZONE = [
    # 'storage',
    # 'processor',
    # 'power-supply',
    # 'graphic-card',
    'motherboard',
    # 'memory'
]

PAGE_COUNT_TECH_ZONE = 3
PAGE_PARAMETER_TECH_ZONE = "/page/"

def generate_url_list_tech_zone() -> List[str]:
    url_list = []
    for category in CATEGORIES_TECHZONE:
        for page in range(1, PAGE_COUNT_TECH_ZONE+1):
            url_list.append(BASE_URL_TECH_ZONE + category +PAGE_PARAMETER_TECH_ZONE+str(page))
    return url_list