import numpy as np
from astropy.io import fits
from datetime import datetime
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

def read_all_files(dirpath: str):
    filenames = get_list_of_files(dirpath)
    dates = []
    arrays = []
    i = 0

    for filename in filenames:
        i += 1

        if i % 100 == 0:
            print('{}: {}'.format(i, filename))
        format = 'MAP%Y-%m-%dT%H-%M-%S.%f.fits'
        curr_date = datetime.strptime(filename, format)

        curr_filename = os.path.join(dirpath, filename)
        curr_data = read_fits(curr_filename)
        tz = pytz.timezone('Europe/Moscow')
        curr_date = curr_date.replace(tzinfo=pytz.utc).astimezone(tz)

        dates.append(curr_date)
        arrays.append(curr_data)
        dates, arrays = (list(t) for t in zip(*sorted(zip(dates, arrays))))

    return (
        np.asarray(dates),
        np.asarray(arrays)
    )

dirpath = 'maps/irmaps/'
(dates, data) = read_all_files(dirpath)
result = fits.PrimaryHDU(data)
result.writeto('result.fits', overwrite=True)