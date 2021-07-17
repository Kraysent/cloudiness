from abc import ABC, abstractmethod

from utils.calibration_parameters import CalibrationParameters


class CalibrationParametersManager(ABC):
    @abstractmethod
    def get_current_calibration(self) -> CalibrationParameters:
        pass

class StandartCalibrationManager(CalibrationParametersManager):
    def get_current_calibration(self) -> CalibrationParameters:
        return CalibrationParameters.read_from_csv(
            ['calibration/k_clear.csv', 'calibration/b_clear.csv',
            'calibration/k_cloud.csv', 'calibration/b_cloud.csv',
            'calibration/k_fog.csv', 'calibration/b_fog.csv',
            'calibration/weights.csv']
        )
