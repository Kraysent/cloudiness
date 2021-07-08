import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

filename = 'uk/MAP2021-04-29T10-45-17.422.fits'

data = fits.getdata(filename)

plt.imshow(data)
