from divisor import divide_cube
import os
from datetime import datetime
from typing import Callable
import matplotlib.pyplot as plt
import numpy as np
import pytz

from fits_compressor import get_fits_date_format, read_fits
from read_pickle import get_field_from_pickle

def plot_picture(filename: str):
    data = read_fits(filename)
    plt.imshow(data)
    plt.show()

def plot_difference(filename1: str, filename2: str):
    data1 = read_fits(filename1)
    data2 = read_fits(filename2)
    diff = data2 - data1
    plt.imshow(diff)
    plt.show()

def get_list_of_files(dirpath: str) -> list:
    result = []
    for (_, _, filenames) in os.walk(dirpath):
        result = filenames
        break

    return sorted(result)

def get_dates_from_fits(dates) -> np.ndarray:
    dates = dates[7:]
    dates = dates.split(',')
    dates = [datetime.strptime(date, get_fits_date_format()) for date in dates]
    dates = np.array(dates)

    return dates

def read_list_of_fits_in_dir(dirpath: str):
    filenames = get_list_of_files(dirpath)[:3]
    results = []
    dates = []

    for filename in filenames:
        print('reading: {}'.format(filename))
        curr_filename = os.path.join(dirpath, filename)
        (curr_data, headers) = read_fits(curr_filename, ['DATES'])
        
        results.append(curr_data)
        dates.append(get_dates_from_fits(headers['DATES']))

    results = np.concatenate(results, axis = 0)
    dates = np.concatenate(dates)

    return dates, results

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

        format = 'MAP%Y-%m-%dT%H-%M-%S.%f.fits'
        curr_date = datetime.strptime(filename, format)

        if date_condition(curr_date):
            curr_filename = os.path.join(dirpath, filename)
            curr_data = read_fits(curr_filename)
            curr_result = expression(curr_data)

            if res_condition(curr_result):
                tz = pytz.timezone('Europe/Moscow')
                curr_date = curr_date.replace(tzinfo=pytz.utc).astimezone(tz)

                dates.append(curr_date)
                results.append(curr_result)
                
    return (dates, results)

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
        pass

    plt.xlim(-40, 15)
    plt.ylim(-30, 15)
    plt.plot(temps1, min_temps, 'ro', markersize = 0.5)
    plt.show()

def run1():
    dirpath = 'maps/'
    (dates, data) = read_list_of_fits_in_dir(dirpath)
    splitted_data = divide_cube(data, 8, 8)

    _, axs = plt.subplots(8, 8)
    num = 1000

    plt.suptitle(dates[num].strftime(get_fits_date_format()))

    for i in range(axs.shape[0]):
        for j in range(axs.shape[1]):
            axs[i, j].imshow(splitted_data[num][i, j])

    plt.show()

run1()
