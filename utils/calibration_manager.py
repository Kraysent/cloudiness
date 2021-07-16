from abc import ABC, abstractmethod

from utils.calibration import Calibration


class CalibrationManager(ABC):
    @abstractmethod
    def get_current_calibration(self) -> Calibration:
        pass

class StandartCalibrationManager(CalibrationManager):
    def get_current_calibration(self) -> Calibration:
        return Calibration.read_from_csv(
            ['calibration/k_clear.csv', 'calibration/b_clear.csv',
            'calibration/k_cloud.csv', 'calibration/b_cloud.csv',
            'calibration/k_fog.csv', 'calibration/b_fog.csv',
            'calibration/weights.csv']
        )
