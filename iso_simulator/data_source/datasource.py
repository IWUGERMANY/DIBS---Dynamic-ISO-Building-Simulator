from abc import ABC, abstractmethod


class DataSource(ABC):

    @abstractmethod
    def getBuildingData(self):
        pass
