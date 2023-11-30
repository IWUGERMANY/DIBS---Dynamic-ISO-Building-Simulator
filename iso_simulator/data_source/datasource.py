from abc import ABC, abstractmethod

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
    def get_tek(self, hk_geb: str, uk_geb: str):
        pass

    @abstractmethod
    def get_weather_data(self, epwfile_path: str):
        pass

    @abstractmethod 
    def get_epw_file(self, plz: str, weather_period: str):
        pass

    @abstractmethod
    def get_usage_time(self, hk_geb: str, uk_geb: str, usage_from_norm: str):
        pass

    @abstractmethod
    def get_gains(self, hk_geb, uk_geb, profile_from_norm, gains_from_group_values):
        pass

    