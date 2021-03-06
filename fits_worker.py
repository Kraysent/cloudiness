from typing import Tuple
import numpy as np
from astropy.io import fits
import os
from datetime import datetime
from utils import utils

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

    def read_all_files(dirpath: str, span_start: int, span_end: int):
        filenames = utils.get_list_of_files(dirpath)[span_start:span_end]
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
        number_of_files = len(utils.get_list_of_files(dirpath))
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

