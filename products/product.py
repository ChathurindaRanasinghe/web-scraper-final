import json

from products.cpu import find_cpu
from products.gpu import find_gpu
from products.power_supply import find_power_supply

from .storage import find_storage
import pandas as pd
import numpy as np

class Product:
    def __init__(self) -> None:
        self.name: str = ''
        self.prices: dict = {}
        self.shops: dict = {}
        self.specs: dict = {}
        self.brand: str = ''
        self.availability: dict = {}
        self.links: dict = {}
        self.category: str = ''
        self.index: int = -1

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


def find_product_index(category: str, name: str, df: pd.DataFrame, name_arr = None, capacity_arr = None ) -> int:
    if category == "storage":
        return find_storage(name=name,df=df,name_arr=name_arr,capacity_arr=capacity_arr)
    elif category == "cpu":
        return find_cpu(name=name,df=df,name_arr=name_arr)
    elif category == "power-supply":
        return find_power_supply(name=name,df=df,name_arr=name_arr,capacity_arr=capacity_arr)
    elif category == "gpu":
        return find_gpu(name=name,df=df,name_arr=name_arr,capacity_arr=capacity_arr)


def init_products() -> dict:
    products = {
        "storage": init_products_storage(),
        "cpu": init_products_cpu(),
        "power-supply": init_products_power_supply(),
        "motherboard": init_products_motherboard(),
        "gpu": init_products_gpu(),
        "memory": init_products_cpu()
    }

    return products

# TODO: optimize
def init_products_storage():
    storage = []
    df = pd.read_csv("base_data/storage_base_data.csv")
    name_arr= (df[ "Name1"]).to_numpy()
    for index in range(len(df.index)):
        product = Product()
        product.name = name_arr[index]
        product.brand = name_arr[index].split()[0]
        product.category = "storage"
        product.index = index
        storage.append(product)
    return storage


def init_products_cpu():
    cpu = []
    df = pd.read_csv("base_data/cpu_base_data.csv")
    name_arr= (df[ "Name1"]).to_numpy()
    for index in range(len(df.index)):
        product = Product()
        product.name = name_arr[index]
        product.category = "cpu"
        product.index = index
        cpu.append(product)
    return cpu


def init_products_power_supply():
    power_supply = []
    df = pd.read_csv("base_data/power_supply_base_data.csv")
    name_arr= (df[ "Name1"]).to_numpy()
    for index in range(len(df.index)):
        product = Product()
        product.name = name_arr[index]
        product.category = "power-supply"
        product.index = index
        power_supply.append(product)
    return power_supply

def init_products_motherboard():
    motherboard = []
    df = pd.read_csv("base_data/motherboard_base_data.csv")
    name_arr= (df[ "Name1"]).to_numpy()
    for index in range(len(df.index)):
        product = Product()
        product.name = name_arr[index]
        product.category = "motherboard"
        product.index = index
        motherboard.append(product)
    return motherboard

def init_products_gpu():
    gpu = []
    df = pd.read_csv("base_data/gpu_base_data.csv")
    name_arr= (df[ "Name1"]).to_numpy()
    for index in range(len(df.index)):
        product = Product()
        product.name = name_arr[index]
        product.category = "gpu"
        product.index = index
        gpu.append(product)
    return gpu

def init_products_memory():
    gpu = []
    df = pd.read_csv("base_data/memory_base_data.csv")
    name_arr= (df[ "Name1"]).to_numpy()
    for index in range(len(df.index)):
        product = Product()
        product.name = name_arr[index]
        product.category = "gpu"
        product.index = index
        gpu.append(product)
    return gpu

