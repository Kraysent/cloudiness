from datetime import timedelta
import sys
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
import matplotlib

from divisor import divide_cube
from fits_worker import FITSWorker, get_list_of_files
import utils.utils as utils

np.set_printoptions(threshold=sys.maxsize, floatmode = 'unique')

def dump_data(data: dict, output_filename: str):
    res_df = DataFrame.from_dict(data)
    res_df.to_pickle(output_filename)

def compress_fits():
    dirpath = 'maps/irmaps/'
    N = 100

    FITSWorker.compress(dirpath, N)

def process_data(data: np.ndarray, ncols: int, nrows: int) -> Tuple[np.ndarray, np.ndarray]:
    splitted_data = divide_cube(data, ncols, nrows)
    return (splitted_data.mean(axis = (3, 4)) / 10, splitted_data.std(axis = (3, 4)) / 10)

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

def filter_temps(dates: np.ndarray, temps: np.ndarray):
    mask = temps != np.NaN
    print(temps.shape, mask.shape)
    return (dates[mask], temps[mask])

def crossmatch_dates():
    pass

def run2():
    filenames = get_list_of_files('maps/', print_full_paths = True)[:7]
    (dates_sky, data) = FITSWorker.concat_list_of_fits(filenames)
    # (data, _) = FITSWorker.read_fits('maps/misc/resultold.fits')
    # dates_sky = FITSWorker.get_list_of_dates('maps/2021/')

    ncols = 8
    nrows = 8
    (temps_sky, temps_sky_disp) = process_data(data, ncols, nrows)

    (dates_temp, temps) = utils.get_field_from_pickle('temperature/all_data.pkl', 'TEMP')
    dates_temp = dates_temp.to_pydatetime().astype(np.datetime64)
    min_temps = np.zeros((len(dates_sky)))

    # N = 20
    # step = int(len(dates_sky) / N)
    # mask = np.zeros((len(dates_sky)), dtype = bool)

    # for i in range(N):
    #     print(i)
    #     diff_matrix = dates_sky[i * step : (i + 1) * step] - dates_temp[:, np.newaxis]
    #     mask[i * step : (i + 1) * step] = np.argmin(diff_matrix, axis = 1)

    # min_temps = temps[mask]

    for i in range(len(dates_sky)):
        if i % 1000 == 0: print(i)
        dates_diff = np.abs(dates_sky[i] - dates_temp)
        min_diff = np.argmin(dates_diff)

        if dates_diff[min_diff] < timedelta(minutes = 10):
            min_temps[i] = temps[min_diff]
        else:
            min_temps[i] = np.nan

    filter = np.logical_not(np.isnan(min_temps))

    dump = {}
    dump['DATE'] = dates_sky[filter]
    dump['TEMP'] = min_temps[filter]

    for i in range(ncols):
        for j in range(nrows):
            dump['TEMP_SKY_{}_{}'.format(i, j)] = temps_sky[:, i, j][filter]
            dump['STD_{}_{}'.format(i, j)] = temps_sky_disp[:, i, j][filter]
        
    dump_data(dump, 'pickles/res.pkl')

def run3():
    filename = 'pickles/res.pkl'

    def plotall():
        (_, dates) = utils.get_field_from_pickle(filename, 'DATE')
        (_, temps) = utils.get_field_from_pickle(filename, 'TEMP')
        
        _, axes = plt.subplots(8, 8)

        for i in range(0, 8):
            for j in range(0, 8):
                (_, temps_sky) = utils.get_field_from_pickle(filename, 'TEMP_SKY_{}_{}'.format(i, j))
                axes[i, j].plot(temps_sky, temps, 'bo', markersize = 0.002)

        plt.xlim(-45, 10)
        plt.ylim(-25, 15)
        plt.show()

    utils.draw_calibration_data(filename)
    plt.show()

# run2()
run3()
