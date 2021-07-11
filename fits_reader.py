from divisor import divide_cube
from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame

from fits_worker import FITSWorker, get_list_of_files
from read_pickle import get_field_from_pickle

def dump_data(data: dict, output_filename: str):
    res_df = DataFrame.from_dict(data)
    res_df.to_pickle(output_filename)

def compress_fits():
    dirpath = 'maps/irmaps/'
    N = 100

    FITSWorker.compress(dirpath, N)

def process_data(data: np.ndarray, ncols: int, nrows: int) -> Tuple[np.ndarray, np.ndarray]:
    splitted_data = divide_cube(data, ncols, nrows)
    return splitted_data.mean(axis = (3, 4)) / 10

def run1():
    filenames = get_list_of_files('maps/', print_full_paths = True)[:3]
    (dates, data) = FITSWorker.concat_list_of_fits(filenames)
    splitted_data = divide_cube(data, 8, 8)

    _, axs = plt.subplots(8, 8)
    num = 1000

    plt.suptitle(dates[num].strftime(FITSWorker.fits_date_format))

    for i in range(axs.shape[0]):
        for j in range(axs.shape[1]):
            axs[i, j].imshow(splitted_data[num][i, j])

    plt.show()

def run2():
    filenames = get_list_of_files('maps/', print_full_paths = True)[:4]
    (dates1, data) = FITSWorker.concat_list_of_fits(filenames)
    # (data, _) = FITSWorker.read_fits('maps/misc/resultold.fits')
    # dates1 = FITSWorker.get_list_of_dates('maps/2021/')

    ncols = 8
    nrows = 8
    temps1 = process_data(data, ncols, nrows)

    (dates2, temps2) = get_field_from_pickle('temperature/all_data.pkl', 'TEMP')
    min_temps = np.zeros((len(dates1)))

    for i in range(len(dates1)):
        if i % 1000 == 0: print(i)
        dates_diff = np.abs(dates1[i] - dates2)
        min_temps[i] = temps2[np.argmin(dates_diff)]

    dump = {}
    dump['DATE'] = dates1
    dump['TEMP'] = min_temps

    for i in range(ncols):
        for j in range(nrows):
            dump['TEMP_SKY_{}_{}'.format(i, j)] = temps1[:, i, j]
        
    dump_data(dump, 'pickles/result.pkl')

def run3():
    filename = 'pickles/result.pkl'
    (_, dates) = get_field_from_pickle(filename, 'DATE')
    (_, temps) = get_field_from_pickle(filename, 'TEMP')
    (_, temps_sky_33) = get_field_from_pickle(filename, 'TEMP_SKY_0_0')

    plt.plot(temps_sky_33, temps, 'ro', markersize = 0.3)
    plt.xlim(-45, 10)
    plt.ylim(-25, 15)
    plt.show()

run3()
