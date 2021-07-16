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

def divide_cube(cube, shape):
    pass
