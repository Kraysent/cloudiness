import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

def plot_picture(filename: str):
    data = fits.getdata(filename)
    plt.imshow(data)
    plt.show()

def plot_difference(filename1: str, filename2: str):
    data1 = fits.getdata(filename1)
    data2 = fits.getdata(filename2)
    diff = data2 - data1
    plt.imshow(diff)
    plt.show()

plot_picture('maps/2021/MAP2021-04-01T00-01-03.016.fits')
plot_difference('maps/2021/MAP2021-04-01T00-01-03.016.fits', 'maps/2021/MAP2021-04-01T00-03-07.767.fits')
