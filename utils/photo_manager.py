from abc import ABC, abstractmethod

import numpy as np

from iotools.fitsio import FITSIO


class PhotoManager(ABC):
    @abstractmethod
    def get_current_photo(self) -> np.ndarray:
        pass

class BlankPhotoManager(PhotoManager):
    def get_current_photo(self) -> np.ndarray:
        return np.ones((64, 64))

class FITSPhotoManager(PhotoManager):
    def get_current_photo(self) -> np.ndarray:
        return FITSIO.get_data('input/current.fits') / 10
