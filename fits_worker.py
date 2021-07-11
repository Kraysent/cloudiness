from typing import Tuple
import numpy as np
from astropy.io import fits
import os
from datetime import datetime

import pytz

def get_list_of_files(dirpath: str, print_full_paths: bool = False) -> list:
    result = []
    for (_, _, filenames) in os.walk(dirpath):
        result = filenames
        break

    if print_full_paths:
        result = [os.path.join(dirpath, fname) for fname in result]
    
    return sorted(result)

class FITSWorker:
    def read_fits(filename: str, headers: list = []) -> Tuple[np.ndarray, list]:
        data = np.zeros((64, 64))
        with fits.open(filename) as hdul:
            data = hdul[0].data

        output_headers = {}

        for h in headers:
            output_headers[h] = hdul[0].header[h]

        return (data, output_headers)

    fits_date_format = '%d-%m-%Y-%H-%M-%S.%f'
    fits_filename_format = 'MAP%Y-%m-%dT%H-%M-%S.%f.fits'

    def get_dates_from_fits(dates: str) -> np.ndarray:
        dates = dates[7:]
        dates = dates.split(',')
        tz = pytz.timezone('Europe/Moscow')
        dates = [
            datetime.strptime(date, FITSWorker.fits_date_format).replace(tzinfo = pytz.utc).astimezone(tz) 
        for date in dates]
        dates = np.array(dates)

        return dates

    def get_list_of_dates(dirpath: str) -> np.ndarray:
        lst = get_list_of_files(dirpath)
        tz = pytz.timezone('Europe/Moscow')
        dates = [
            datetime.strptime(date, FITSWorker.fits_filename_format).replace(tzinfo = pytz.utc).astimezone(tz) 
        for date in lst]

        return np.array(sorted(dates))

    def concat_list_of_fits(filenames: list) -> Tuple[np.ndarray, np.ndarray]:
        results = []
        dates = []

        for filename in filenames:
            print('reading: {}'.format(filename))
            (curr_data, headers) = FITSWorker.read_fits(filename, ['DATES'])

            results.append(curr_data)
            dates.append(FITSWorker.get_dates_from_fits(headers['DATES']))

        results = np.concatenate(results, axis = 0)
        dates = np.concatenate(dates)

        return dates, results

    def read_all_files(dirpath: str, span_start: int, span_end: int):
        filenames = get_list_of_files(dirpath)[span_start:span_end]
        number_of_files = len(filenames)

        dates = np.zeros((number_of_files), datetime)
        arrays = np.zeros((number_of_files, 64, 64))
        i = 0

        for filename in filenames:
            format = FITSWorker.fits_filename_format
            curr_date = datetime.strptime(filename, format)

            curr_filename = os.path.join(dirpath, filename)
            (curr_data, _) = FITSWorker.read_fits(curr_filename)

            dates[i] = curr_date
            arrays[i] = curr_data

            i += 1

            if i % 100 == 0:
                print('{}: {}'.format(i, filename))

        perm = dates.argsort()

        return (dates[perm], arrays[perm])

    def compress(dirpath: str, number_of_res_files: int, file_prefix: str = 'result'):
        number_of_files = len(get_list_of_files(dirpath))
        step = int(number_of_files / number_of_res_files)

        for i in range(number_of_res_files):
            print(i)
            (dates, data) = FITSWorker.read_all_files(dirpath, i * step, (i + 1) * step)

            result = fits.PrimaryHDU(data)
            result.header['DATES'] = ''
            format = FITSWorker.fits_date_format
            first = True
            for d in dates:
                if not first:
                    result.header['DATES'] += ','

                result.header['DATES'] += d.strftime(format)
                first = False

            result.writeto('{}{}.fits'.format(file_prefix, i), overwrite=True)

