from abc import ABC, abstractmethod

from iotools import jsonio
from iotools import webio


class TemperatureManager(ABC):
    @abstractmethod
    def get_current_temperature(self) -> float:
        pass

class BlankTemperatureManager(TemperatureManager):
    def get_current_temperature(self) -> float:
        return -10.0

class WebTemperatureManager(TemperatureManager):
    url = 'http://192.168.10.110/get_ocs_data/'

    def get_current_temperature(self) -> float:
        webresp = webio.get_response(self.url)
        res = jsonio.read_json(webresp)
        return float(res['TOUT'])
