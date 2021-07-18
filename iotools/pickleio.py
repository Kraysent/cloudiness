import pandas as pd
import numpy as np

def get_field(filename: str, field: str) -> np.ndarray:
    data  = pd.read_pickle(filename)
    res = data[field].to_numpy()

    return res

def get_index(filename: str) -> np.ndarray:
    data = pd.read_pickle(filename)

    return data.index.to_numpy()

def dump_dict(filename: str, data: dict):
    res_df = pd.DataFrame.from_dict(data)
    res_df.to_pickle(filename)