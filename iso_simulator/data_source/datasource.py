import pandas as pd
from abc import ABC, abstractmethod
from typing import Union, Tuple, List
from iso_simulator.model.weather_data import WeatherData
from iso_simulator.model.epw_file import EPWFile


class DataSource(ABC):

    @abstractmethod
    def get_building_data(self):
        pass

    @abstractmethod
    def get_epw_pe_factors(self):
        pass

    @abstractmethod
    def get_schedule(self, hk_geb: str, uk_geb: str):
        pass

    @abstractmethod
    def get_schedule_sum(self, hk_geb: str, uk_geb: str) -> float:
        pass

    @abstractmethod
    def get_tek(self, hk_geb: str, uk_geb: str) -> Union[Tuple[float, str], ValueError]:
        pass

    @abstractmethod
    def get_weather_data(self, epw_file_path: str) -> List[WeatherData]:
        pass

    @abstractmethod
    def choose_and_get_the_right_weather_data_from_path(self, weather_period, file_name) -> List[WeatherData]:
        pass

    @abstractmethod
    def get_epw_file(self, plz: str, weather_period: str) -> EPWFile:
        pass

    @abstractmethod
    def get_usage_time(self, hk_geb: str, uk_geb: str, usage_from_norm: str) -> Union[Tuple[int, int], ValueError]:
        pass

    @abstractmethod
    def get_gains(self, hk_geb: str, uk_geb: str, profile_from_norm: str, gains_from_group_values: str) -> Tuple[
        Tuple[float, str], float]:
        pass

    @abstractmethod
    def result_to_pandas_dataframe(self, result) -> pd.DataFrame:
        pass

    @abstractmethod
    def results_pandas_dataframe_to_excel(self, dataframe: pd.DataFrame) -> None:
        pass
