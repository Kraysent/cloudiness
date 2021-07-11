import numpy as np

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

def divide_cube_test():
    init_array = np.zeros((20, 64, 64))
    res = divide_cube(init_array, 8, 8)
    assert res == np.zeros((20, 8, 8, 8, 8))