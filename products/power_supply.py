from typing import Dict, Union
import pandas as pd
from fuzzywuzzy import fuzz
import numpy as np
import re

def extract_wattage_from_name(name: str) -> int:
    try:
        wattage = re.findall(r'\d{3,4}w|\d{3,4} w|hx\d{3,4}', name.lower())[0].strip()
    except IndexError:
        return 0
    
    return int(re.findall(r'\d+',wattage)[0])
        
    


def find_power_supply(name: str, df: pd.DataFrame, name_arr: np.ndarray, capacity_arr: np.ndarray ) -> Union[int, int]:
    capacity = extract_wattage_from_name(name)
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


# FormFactor,EfficiencyRating,Wattage,Modular
def get_power_supply_specs(index:int, df:pd.DataFrame) -> Dict:
    specs = {}
    specs['form-factor'] = df.loc[index,'FormFactor']
    specs['efficiency-rating'] = df.loc[index,'EfficiencyRating']

    if str(specs['efficiency-rating']) == 'nan':
        specs['efficiency-rating'] = 'not-available'

    specs['wattage'] = int(df.loc[index,'Wattage'])
    specs['modular'] = df.loc[index,'Modular']
    return specs
