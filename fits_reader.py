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

def read_all_files(dirpath: str, reader: Callable = lambda x: x):
    '''This function reads all files and takes some data from them: for each 
    file, reader lambda is called. Input for this lambda is read_fits() for 
    each file. Result of this function would be tuple of dates and results of 
    lambda for each day. By default it returns (dates, data_for_each_day)'''
    filenames = get_list_of_files(dirpath)
    dates = []
    results = []
    i = 0

    for filename in filenames:
        i += 1

        if i % 50 == 0:
            print('{}: {}'.format(i, filename))

        curr_filename = os.path.join(dirpath, filename)
        curr_data = read_fits(curr_filename)

        format = 'MAP%Y-%m-%dT%H-%M-%S.%f.fits'
        curr_date = datetime.strptime(filename, format)
        tz = pytz.timezone('Europe/Moscow')
        curr_date = curr_date.replace(tzinfo=pytz.utc).astimezone(tz)

        dates.append(curr_date)
        results.append(reader(curr_data))

    return (dates, results)

def read_temps(data: np.ndarray) -> int: 
    return data[
        int(data.shape[0] / 2), 
        int(data.shape[1] / 2) 
    ]

dirpath = 'maps/2021/'

(dates1, temps1) = read_all_files(dirpath, read_temps)
(dates2, temps2) = get_field_from_pickle('temperature/all_data.pkl', 'TEMP_SKY')
min_temps = []

for i in range(len(dates1)):
    if i % 50 == 0:
        print('{}'.format(i))

    dates_diff = np.abs(dates2 - dates1[i])
    min_temps.append(temps2[np.argmin(dates_diff)])
    pass

plt.plot(temps1, min_temps, 'ro', markersize = 0.5)
plt.show()
