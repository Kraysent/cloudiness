from numpy.core.getlimits import MachArLike
from numpy.lib.shape_base import _split_dispatcher
from divisor import divide_cube
from typing import Tuple
import os
from datetime import datetime
from typing import Callable
import matplotlib.pyplot as plt
import numpy as np
import pytz

from fits_worker import FITSWorker, get_list_of_files
from read_pickle import get_field_from_pickle

def compress_fits():
    dirpath = 'maps/irmaps/'
    N = 100

    FITSWorker.compress(dirpath, N)

def read_all_files(
    dirpath: str, 
    expression: Callable = lambda x: x, 
    date_condition: Callable = lambda x: True, 
    res_condition: Callable = lambda x: True
):
    filenames = get_list_of_files(dirpath)
    dates = []
    results = []
    i = 0

    for filename in filenames:
        i += 1

        if i % 50 == 0:
            print('{}: {}'.format(i, filename))

        format = FITSWorker.fits_filename_format
        curr_date = datetime.strptime(filename, format)

        if date_condition(curr_date):
            curr_filename = os.path.join(dirpath, filename)
            curr_data = FITSWorker.read_fits(curr_filename)
            curr_result = expression(curr_data)

            if res_condition(curr_result):
                tz = pytz.timezone('Europe/Moscow')
                curr_date = curr_date.replace(tzinfo=pytz.utc).astimezone(tz)

                dates.append(curr_date)
                results.append(curr_result)
                
    return (dates, results)

def process_data(data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    splitted_data = divide_cube(data, 8, 8)
    return splitted_data.mean(axis = (3, 4)) / 10

def read_temps(data: np.ndarray) -> int: 
    return data[
        int(data.shape[0] / 2), 
        int(data.shape[1] / 2) 
    ] / 10

def is_night(dt: datetime) -> bool:
    return dt.hour > 0 and dt.hour < 5

def run():
    dirpath = 'maps/irmaps/'

    (dates1, temps1) = read_all_files(dirpath, read_temps, is_night)
    (dates2, temps2) = get_field_from_pickle('temperature/all_data.pkl', 'TEMP')
    min_temps = []

    for i in range(len(dates1)):
        if i % 50 == 0:
            print('{}'.format(i))

        dates_diff = np.abs(dates2 - dates1[i])
        min_temps.append(temps2[np.argmin(dates_diff)])

    plt.xlim(-40, 15)
    plt.ylim(-30, 15)
    plt.plot(temps1, min_temps, 'ro', markersize = 0.5)
    plt.show()

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
    temps1 = process_data(data)

    (dates2, temps2) = get_field_from_pickle('temperature/all_data.pkl', 'TEMP')
    min_temps = np.zeros((len(dates1)))

    for i in range(len(dates1)):
        if i % 1000 == 0: print(i)
        dates_diff = np.abs(dates1[i] - dates2)
        min_temps[i] = temps2[np.argmin(dates_diff)]

    ncols = 8
    nrows = 8
    _, axes = plt.subplots(ncols, nrows)

    for i in range(ncols):
        for j in range(nrows):
            axes[i, j].plot(temps1[:, i, j], min_temps[:], 'ro', markersize = 0.05)
            axes[i, j].set_xlim(-40, 15)
            axes[i, j].set_ylim(-30, 15)

    plt.show()

run2()
