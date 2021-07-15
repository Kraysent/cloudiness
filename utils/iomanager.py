from abc import ABC, abstractmethod

from utils.calibration import CalibrationIOManager
from utils.fitsiomanager import FITSIOManager


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

class BlankIOManager(IOManager):
    def __init__(self):
        pass
    
    def get_current_photo(self):
        return FITSIOManager.get_data('input/current.fits') / 10

    def get_current_calibration(self):
        return CalibrationIOManager.read_calibration_from_csv(
            ['calibration/k_clear.csv', 'calibration/b_clear.csv',
            'calibration/k_cloud.csv', 'calibration/b_cloud.csv',
            'calibration/k_fog.csv', 'calibration/b_fog.csv',
            'calibration/weights.csv']
        )

    def get_current_temperature(self):
        return -20
