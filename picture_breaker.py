import matplotlib.pyplot as plt
from fits_reader import read_fits
import numpy as np

def get_all_cells(pic: np.ndarray, n_cols: int, n_rows: int) -> list:
    width = pic.shape[0]
    height = pic.shape[1]

    width_step = int(width / n_cols)
    height_step = int(height / n_rows)

    result = []

    for i in range(n_cols):
        result.append([])

        for j in range(n_rows):
            result[i].append(pic[
                i * width_step : (i + 1) * width_step,
                j * height_step : (j + 1) * height_step,
            ])

    return result

n_rows = 8
n_cols = 8
cells = get_cells(read_fits('maps/2021/MAP2021-04-01T00-01-03.016.fits'), n_cols, n_rows)
fig, axs = plt.subplots(n_cols, n_rows)

for i in range(len(cells)):
    for j in range(len(cells[0])):
        axs[i, j].imshow(cells[i][j])

plt.show()
