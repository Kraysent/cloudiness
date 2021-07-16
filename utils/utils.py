import numpy as np
import pandas as pd

def divide(photo, shape):
    fragment_shape = (
        int(photo.shape[0] / shape[0]), 
        int(photo.shape[1] / shape[1])
    )
    result = np.zeros((shape[0], shape[1], fragment_shape[0], fragment_shape[1]))

    for i in range(shape[0]):
        for j in range(shape[1]):
            result[i, j] = photo[
                i * fragment_shape[0]: (i + 1) * fragment_shape[0],
                j * fragment_shape[1]: (j + 1) * fragment_shape[1]
            ]

    return result

def get_field_from_pickle(filename: str, field: str) -> tuple:
    data  = pd.read_pickle(filename)
    dates = data.index
    res = data[field].to_numpy()

    return (dates, res)
    