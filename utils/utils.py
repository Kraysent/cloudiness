import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

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

def draw_calibration_data(filename: str, clogscale: bool = True):
    (_, dates) = get_field_from_pickle(filename, 'DATE')
    (_, temps) = get_field_from_pickle(filename, 'TEMP')
    (_, temps_sky) = get_field_from_pickle(filename, 'TEMP_SKY_4_4')
    (_, temps_sky_disp) = get_field_from_pickle(filename, 'STD_1_2')

    norm = None
    
    if clogscale:
        norm = matplotlib.colors.LogNorm()

    plt.scatter(
        temps_sky, temps, 
        s = 0.1, c = temps_sky_disp, 
        cmap = 'plasma', norm = norm
    )

    plt.xlim(-45, 10)
    plt.ylim(-25, 15)
    plt.colorbar()
    plt.show()
