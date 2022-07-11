from typing import Dict, Union
import pandas as pd
from fuzzywuzzy import fuzz
import numpy as np


def find_cpu(name: str, df: pd.DataFrame, name_arr: np.ndarray) -> Union[int,int]:
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

def get_cpu_specs(index:int, df:pd.DataFrame) -> Dict:
    specs = {}
    specs['core-count'] = int(df.loc[index,'CoreCount'])
    specs['performance-core-clock'] = df.loc[index, 'PerformanceCoreClock']

    specs['performance-boost-clock'] = df.loc[index,'PerformanceBoostClock']

    if str(specs['performance-boost-clock']) == 'nan':
        specs['performance-boost-clock'] = 0.0
    
    specs['tdp'] = int(df.loc[index,'TDP'])
    specs['integrated-graphics'] = df.loc[index,'IntegratedGraphics']
    specs['simultaneous-multithreading'] = df.loc[index,'SMT']

    return specs

    