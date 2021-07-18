import os
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Tuple

import numpy as np
from iotools import fitsio

from utils import utils


class PhotoManager(ABC):
    @abstractmethod
    def get_current_photo(self) -> np.ndarray:
        pass

    @abstractmethod
    def get_historical_photo_data(self) -> Tuple[np.ndarray, np.ndarray]:
        pass

class BlankPhotoManager(PhotoManager):
    def get_current_photo(self) -> np.ndarray:
        return np.ones((64, 64))

    def get_historical_photo_data(self) -> Tuple[np.ndarray, np.ndarray]:
        return (np.array([
            datetime(2021, 5, 5) + timedelta(days = 1 * i, hours = 5 * i) 
            for i in range(10)]), np.ones((10, 64, 64))
        )

class FITSPhotoManager(PhotoManager):
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def get_current_photo(self) -> np.ndarray:
        return fitsio.get_data(self.filename) / 10

    def get_historical_photo_data(self) -> Tuple[np.ndarray, np.ndarray]:
        dirpath = 'maps/'
        slice = (0, 1)
        list_of_files = utils.get_list_of_files(dirpath)[slice[0]: slice[1]]
        data = []
        dates = []

        for filename in list_of_files:
            print('reading: {}'.format(filename))
            (curr_data, headers) = fitsio.get_data(os.path.join(dirpath, filename), ['DATES'])
            curr_dates = utils.get_dates_from_fits(headers['DATES'])
            data.append(curr_data)
            dates.append(curr_dates)

        data = np.concatenate(data, axis = 0)
        dates = np.concatenate(dates).astype(np.datetime64)

        return (dates, data)
