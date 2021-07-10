import numpy as np
from astropy.io import fits
from datetime import date, datetime
import os
import pytz

def compress():
    pass

def read_fits(filename: str) -> np.ndarray:
    data = np.zeros((64, 64))
    with fits.open(filename) as hdul:
        data = hdul[0].data.copy()

    return data

def get_list_of_files(dirpath: str) -> list:
    result = []
    for (_, _, filenames) in os.walk(dirpath):
        result = filenames
        break

    return result

def read_all_files(dirpath: str, span_start: int, span_end: int):
    filenames = get_list_of_files(dirpath)[span_start:span_end]
    number_of_files = len(filenames)

    dates = np.zeros((number_of_files), datetime)
    arrays = np.zeros((number_of_files, 64, 64))
    i = 0

    for filename in filenames:
        format = 'MAP%Y-%m-%dT%H-%M-%S.%f.fits'
        curr_date = datetime.strptime(filename, format)

        curr_filename = os.path.join(dirpath, filename)
        curr_data = read_fits(curr_filename)

        dates[i] = curr_date
        arrays[i] = curr_data

        i += 1

        if i % 100 == 0:
            print('{}: {}'.format(i, filename))

    perm = dates.argsort()

    return (dates[perm], arrays[perm])

dirpath = 'maps/irmaps/'
number_of_files = len(get_list_of_files(dirpath))
N = 10
step = int(number_of_files / N)

for i in range(N):
    print(i)
    (dates, data) = read_all_files(dirpath, i * step, (i + 1) * step)

    result = fits.PrimaryHDU(data)
    result.header['DATES'] = 'example'
    format = '%d-%m-%Y-%H-%M-%S.%f'
    first = True
    for d in dates:
        if not first:
            result.header['DATES'] += ','

        result.header['DATES'] += d.strftime(format)
        first = False

    result.writeto('result{}.fits'.format(i), overwrite=True)