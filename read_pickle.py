import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_field_from_pickle(filename: str, field: str) -> tuple:
    data  = pd.read_pickle(filename)
    return (data.index, data[field])

(dates, temperature) = get_field_from_pickle('temperature/all_data.pkl', 'TEMP_SKY')
plt.plot(dates, temperature, 'o', markersize = 0.1)
plt.show()