import re
from typing import Union
from fuzzywuzzy import fuzz
import pandas as pd

def extract_capacity_from_name(name: str) -> float:
    try:
        capacity = re.findall(r'\d{1,2}gb|\d{1,2} gb|\d{1,2}g', name.lower())[0]
        if 'gb' in capacity:
            return int(capacity.replace('gb', '').strip())
        return int(capacity.replace('g', '').strip())
        
    except IndexError:
        return 0
   

def extract_chipset_from_name(name: str):
    pass



def find_gpu(name: str, df: pd.DataFrame, name_arr, capacity_arr ) -> Union[int, int]:
    capacity = extract_capacity_from_name(name)
    
    # name = re.sub(r'\d{1,2}gb|\d{1,2} gb|\d{1,2}g','',name)
    
    # if "geforce" in name:
    #         name = name.replace("geforce", "")
    # if "rtx" in name:
    #     name = name.replace("rtx", "")
    # elif "gtx" in name:
    #     name = name.replace("gtx", "")

    # elif "radeon" in name:
    #     name = name.replace("radeon", "")
    # elif "rx" in name:
    #     name = name.replace("rx", "")

    # name = re.sub("[0-9]{3,4}","", name)
    # name = name.replace("  "," ").replace("   "," ")
    
    
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
    # if highest_ratio < 90:
    #     print(name)          
    return index, highest_ratio