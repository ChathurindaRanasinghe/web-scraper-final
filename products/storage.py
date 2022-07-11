import re
from typing import Union
from fuzzywuzzy import fuzz
import pandas as pd
import numpy as np

def extract_capacity_from_name(name: str) -> float:
    try:
        capacity = re.findall(r'\d{1,2}tb|\d{1,4}gb|\d{1,2}\.\dtb|\d{1,4} gb', name.lower())[0]
        if 'tb' in capacity:
            return float(capacity.replace('tb', '').strip()) * 1024
        elif 'gb' in capacity:
            return float(capacity.replace('gb', '').strip())
    except IndexError:
        if '250' in name:
            return 250.0
        elif '256' in name:
            return 256.0
        else:
            pass
            #print(name)
    


def find_storage(name: str, df: pd.DataFrame, name_arr: np.ndarray, capacity_arr: np.ndarray ) -> Union[int, int]:
    capacity = extract_capacity_from_name(name)
    index = None
    highest_ratio = 0
    for i in range(len(df.index)):
        if capacity == capacity_arr[i]:
            ratio = fuzz.partial_ratio(name_arr[i], name)
            if highest_ratio < ratio:
                highest_ratio = ratio
                index = i
                if highest_ratio == 100:
                    return index, highest_ratio
                
    return index, highest_ratio

# def find_storage(name: str) -> Union[int, int]:
#     capacity = extract_capacity_from_name(name)
#     index = None
#     highest_ratio = 0
#     df = pd.read_csv("base_data/storage_base_data.csv")
#     for i in range(len(df.index)):
#         if capacity == df.loc[index,"Capacity"]:
#             ratio = fuzz.partial_ratio(df.loc[index,"Name1"], name)
#             if highest_ratio < ratio:
#                 highest_ratio = ratio
#                 index = i
#                 if highest_ratio == 100:
#                     return index, highest_ratio
#     print(highest_ratio)       
#     return index, highest_ratio


def get_storage_specs(index:int, df: pd.DataFrame) -> dict:
    # print("Inside Storage Specs")
    specs = {}
    specs['capacity'] = df.loc[index,'Capacity']

    specs['type'] = df.loc[index,'Type']
    # if df.loc[index,'Cache'] == '':
    #     specs['cache'] = 0

    specs['cache'] = df.loc[index,'Cache'] # .replace(' MB','')
    # print(type(specs['cache']))
    # print(str(specs['cache']))
    if str(specs['cache']) == 'nan':
        specs['cache'] = 0.0
    
    specs['form-factor'] = df.loc[index,"FormFactor"]
    specs['interface'] = df.loc[index,"Interface"]
    
    # specs['image-url']
    return specs

