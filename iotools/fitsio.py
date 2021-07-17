import numpy as np
from astropy.io import fits


def get_data(filename: str, headers: list = []):
    data = np.zeros((64, 64))

    with fits.open(filename) as hdul:
        data = hdul[0].data

    if headers != []:
        output_headers = {}

        for h in headers:
            output_headers[h] = hdul[0].header[h]

        return (data, output_headers)
    else: 
        return data
        
