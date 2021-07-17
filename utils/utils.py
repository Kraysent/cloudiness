import os
from datetime import datetime, timedelta
from typing import Tuple

import numpy as np
import pytz

fits_date_format = '%d-%m-%Y-%H-%M-%S.%f'
fits_filename_format = 'MAP%Y-%m-%dT%H-%M-%S.%f.fits'

def divide_plane(photo, shape):
    fragment_shape = (
        int(photo.shape[0] / shape[0]), 
        int(photo.shape[1] / shape[1])
    )
    result = np.zeros((shape[0], shape[1], fragment_shape[0], fragment_shape[1]))

    for ix, iy in np.ndindex(shape):
        result[ix, iy] = photo[
            ix * fragment_shape[0]: (ix + 1) * fragment_shape[0],
            iy * fragment_shape[1]: (iy + 1) * fragment_shape[1]
        ]

    return result

def divide_cube(
    cube: np.ndarray, shape: Tuple[int, int]
) -> np.ndarray:
    '''
    * cube: ndarray with shape (number_of_frames, frame_width, frame_height)
    '''
    num_of_frames = cube.shape[0]
    width_step = int(cube.shape[1] / shape[0])
    height_step = int(cube.shape[2] / shape[1])
    res_arr = np.zeros((num_of_frames, shape[0], shape[1], width_step, height_step))

    for frame in range(num_of_frames):
        for col, row in np.ndindex(shape):
            curr_frame = cube[frame]
            res_arr[frame][col, row] = curr_frame[
                col * width_step  : (col + 1) * width_step, 
                row * height_step : (row + 1) * height_step
            ]

    return res_arr

def find_nearest_date(date: datetime, dates: np.ndarray) -> Tuple[int, timedelta]:
    diff_array = np.abs(dates - date)
    index = np.argmin(diff_array)

    return (index, diff_array[index])

def get_statistical_parameters(data: np.ndarray):
    return (data.mean(axis = (3, 4)), data.std(axis = (3, 4)))

def get_list_of_files(dirpath: str, print_full_paths: bool = False) -> list:
    result = []
    for (_, _, filenames) in os.walk(dirpath):
        result = filenames
        break

    if print_full_paths:
        result = [os.path.join(dirpath, fname) for fname in result]
    
    return sorted(result)

def get_dates_from_fits(header_string: str) -> np.ndarray:
    header_string = header_string[7:] # accidental 'example' in the beginning
    dates = header_string.split(',')
    tz = pytz.timezone('Europe/Moscow')
    dates = [
        datetime.strptime(date, fits_date_format).replace(tzinfo = pytz.utc).astimezone(tz) 
    for date in dates]
    dates = np.array(dates)

    return dates

