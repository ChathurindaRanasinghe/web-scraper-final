
from typing import Dict, Union
import pandas as pd
from fuzzywuzzy import fuzz
import numpy as np


def find_motherboard(name: str, df: pd.DataFrame, name_arr: np.ndarray) -> Union[int,int]:
    index = None
    highest_ratio = 0
    for i in range(len(df.index)):
        ratio = fuzz.partial_ratio(name_arr[i], name)
        if highest_ratio < ratio:
            highest_ratio = ratio
            index = i
            if highest_ratio == 100:
                return index, highest_ratio
    return index, highest_ratio


# ,CoreCount,PerformanceCoreClock,PerformanceBoostClock,TDP,IntegratedGraphics,SMT

def get_motherboard_specs(index:int, df:pd.DataFrame) -> Dict:
    specs = {}
    
    

    return specs