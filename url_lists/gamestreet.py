from typing import List

GAMESTREET_WEBSITE = "https://www.gamestreet.lk/"
BASE_URL_GAMESTREET = "https://www.gamestreet.lk/products.php?cat"
CATEGORIES_GAMESTREET = [
    #"=Mg==&scat=MQ==",  # processor
    # "=Mg==&scat=Mw==",  # memory
    #"=Mg==&scat=MTM=",  # storage - ssd
    #"=Mg==&scat=MTE=",  # storage - hdd
    "=Mg==&scat=Mg==",  # motherboard
    # "=Mg==&scat=Ng==",  # graphic cards
    #"=Mg==&scat=NQ==",  # power supply
]


def generate_url_list_gamestreet() -> List[str]:
    url_list = []
    for category in CATEGORIES_GAMESTREET:
        url_list.append(BASE_URL_GAMESTREET+category)
    return url_list
