from datetime import datetime, timedelta
from typing import Tuple

import numpy as np


def divide_plane(photo, shape):
    fragment_shape = (
        int(photo.shape[0] / shape[0]), 
        int(photo.shape[1] / shape[1])
    )
    result = np.zeros((shape[0], shape[1], fragment_shape[0], fragment_shape[1]))

    for i in range(shape[0]):
        for j in range(shape[1]):
            result[i, j] = photo[
                i * fragment_shape[0]: (i + 1) * fragment_shape[0],
                j * fragment_shape[1]: (j + 1) * fragment_shape[1]
            ]

    return result

def divide_cube(
    cube: np.ndarray, ncols: int, nrows: int
) -> np.ndarray:
    '''
    * cube: ndarray with shape (number_of_frames, frame_width, frame_height)
    '''
    num_of_frames = cube.shape[0]
    width_step = int(cube.shape[1] / ncols)
    height_step = int(cube.shape[2] / ncols)
    res_arr = np.zeros((num_of_frames, ncols, nrows, width_step, height_step))

    for frame in range(num_of_frames):
        for col in range(ncols):
            for row in range(nrows):
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

