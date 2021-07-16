from abc import ABC, abstractmethod


class TemperatureManager(ABC):
    @abstractmethod
    def get_current_temperature(self) -> float:
        pass

class BlankTemperatureManager(TemperatureManager):
    def get_current_temperature(self) -> float:
        return -10.0
