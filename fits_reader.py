import os
from typing import Callable
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import pytz
from astropy.io import fits
from read_pickle import get_field_from_pickle

def read_fits(filename: str) -> np.ndarray:
    return fits.getdata(filename)

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

dates = []
center_temps = []

def get_list_of_files(dirpath: str) -> list:
    result = []
    for (_, _, filenames) in os.walk(dirpath):
        result = filenames
        break

    return result

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
