from os import read
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

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

plot_picture('maps/2021/MAP2021-04-01T00-01-03.016.fits')
plot_difference('maps/2021/MAP2021-04-01T00-01-03.016.fits', 'maps/2021/MAP2021-04-01T00-03-07.767.fits')
