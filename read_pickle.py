from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_field_from_pickle(filename: str, field: str) -> tuple:
    data  = pd.read_pickle(filename)
    dates = data.index
    res = data[field].to_numpy()

    return (dates, res)
