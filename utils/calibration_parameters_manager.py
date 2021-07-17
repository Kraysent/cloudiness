from abc import ABC, abstractmethod
from datetime import datetime

from utils.calibration_parameters import CalibrationParameters
import numpy as np
from iotools import pickleio

class CalibrationParametersManager(ABC):
    @abstractmethod
    def get_current_calibration(self) -> CalibrationParameters:
        pass

    def get_list_of_dates(self) -> np.ndarray:
        pass

class StandartCalibrationParametersManager(CalibrationParametersManager):
    def get_current_calibration(self) -> CalibrationParameters:
        return CalibrationParameters.read_from_csv(
            ['calibration/k_clear.csv', 'calibration/b_clear.csv',
            'calibration/k_cloud.csv', 'calibration/b_cloud.csv',
            'calibration/k_fog.csv', 'calibration/b_fog.csv',
            'calibration/weights.csv']
        )

    def get_list_of_dates(self) -> np.ndarray:
        np_dates = pickleio.get_field('pickles/res.pkl', 'DATE')
        return np_dates.astype('M8[ms]').astype('O')
