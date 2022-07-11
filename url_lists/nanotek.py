from typing import List

BASE_URL_NANOTEK = "https://www.nanotek.lk/category/"
CATEGORIES_NANOTEK = [
    "processors",
    # "motherboards",
    # "memory-ram",
    # "graphic-cards",
    "power-supply",
    "storage"
]

PAGE_COUNT_NANOTEK = 10
PAGE_PARAMETER_NANOTEK = "?page="


def generate_url_list_nanotek() -> List[str]:
    url_list = []
    for category in CATEGORIES_NANOTEK:
        for page in range(1, PAGE_COUNT_NANOTEK+1):
            url_list.append(BASE_URL_NANOTEK + category +
                            PAGE_PARAMETER_NANOTEK+str(page))
    return url_list
