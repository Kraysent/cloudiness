from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Tuple

import numpy as np
from iotools import jsonio, webio, pickleio


class TemperatureManager(ABC):
    @abstractmethod
    def get_current_temperature(self) -> float:
        pass

    @abstractmethod
    def get_historical_temperature_data(self) -> Tuple[np.ndarray, np.ndarray]:
        pass

class BlankTemperatureManager(TemperatureManager):
    def get_current_temperature(self) -> float:
        return -10.0

    def get_historical_temperature_data(self) -> Tuple[np.ndarray, np.ndarray]:
        return (
            np.array([datetime(2021, 5, 5) + timedelta(days = 1 * i, hours = 5 * i) for i in range(10)]),
            np.linspace(-10, 17, 10)
        )

class WebTemperatureManager(TemperatureManager):
    url = 'http://192.168.10.110/get_ocs_data/'

    def get_current_temperature(self) -> float:
        webresp = webio.get_response(self.url)
        res = jsonio.read_json(webresp)
        return float(res['TOUT'])

    def get_historical_temperature_data(self) -> Tuple[np.ndarray, np.ndarray]:
        temps = pickleio.get_field('temperature/all_data.pkl', 'TEMP')
        dates_temp = pickleio.get_field('temperature/all_data.pkl', 'DATE')
        dates_temp = dates_temp.to_pydatetime().astype(np.datetime64)
        return (dates_temp, temps)
