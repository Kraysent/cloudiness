from abc import ABC, abstractmethod

from iotools.jsonio import JSONIO
from iotools.webio import WebIO


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
        webresp = WebIO.get_response(self.url)
        res = JSONIO.read_json(webresp)
        return float(res['TOUT'])
