import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
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

dirpath = 'maps/2021/'
filenames = get_list_of_files(dirpath)
i = 0

for filename in filenames:
    i += 1

    if i % 50 == 0:
        print('{}: {}'.format(i, filename))

    curr_filename = os.path.join(dirpath, filename)
    curr_data = read_fits(curr_filename)
    center_temp = curr_data[
        int(curr_data.shape[0] / 2), 
        int(curr_data.shape[1] / 2) 
    ]

    format = 'MAP%Y-%m-%dT%H-%M-%S.%f.fits'
    curr_date = datetime.strptime(filename, format)

    dates.append(curr_date)
    center_temps.append(center_temp)

dates1 = np.array(dates)
temps1 = np.array(center_temps)

(dates2, temps2) = get_field_from_pickle('temperature/all_data.pkl', 'TEMP')

fig, (ax1, ax2) = plt.subplots(nrows = 2)
ax1.plot(dates, center_temps, 'bo', markersize = 0.1)
ax2.plot(dates2, temps2, 'bo', markersize = 0.1)
ax2.set_xlim(ax1.get_xlim())
plt.show()
