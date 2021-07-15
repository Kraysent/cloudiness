from abc import abstractmethod, ABC
from fitsiomanager import FITSIOManager
import numpy as np

class IOManager(ABC):
    @abstractmethod
    def get_current_photo(self):
        pass

    @abstractmethod
    def get_current_temperature(self):
        pass

    @abstractmethod
    def get_current_calibration(self):
        pass

class StandartIOManager(IOManager):
    def get_current_photo(self):
        manager = FITSIOManager()
        return manager.get_data('input/current.fits')

    def get_current_calibration(self):
        return super().get_current_calibration()

    def get_current_temperature(self):
        return 0