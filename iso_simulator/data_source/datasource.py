import os
import pandas as pd
from abc import ABC, abstractmethod
from typing import Union, Tuple, List
from iso_simulator.model.weather_data import WeatherData
from iso_simulator.model.epw_file import EPWFile
from iso_simulator.model.primary_energy_and_emission_factors import PrimaryEnergyAndEmissionFactor
from iso_simulator.model.schedule_name import ScheduleName
from iso_simulator.exceptions.uk_or_hk_exception import HkOrUkNotFoundError


class DataSource(ABC):
    """
    This interface provides several methods that can be implemented in other classes
    """

    @abstractmethod
    def get_user_building(self, path: str):
        """
        This method reads the file which contains the building data to simulate.
        Args:
            path: where the file is located

        Returns:
            building
        Return type:
            Building
        """

    @abstractmethod
    def get_user_buildings(self, path: str):
        """
        This method reads the file which contains the building data to simulate.
        Args:
            path: where the file is located

        Returns:
            building
        Return type:
            list [Building]
        """

    @abstractmethod
    def get_building_data(self, building_id: str):
        """
        This method retrieves one building from the csv file and maps them to objects.
        Args:
            building_id: building to simulate
        Returns:
            building
        Return type:
            Building
        """
        pass

    @abstractmethod
    def get_all_buildings(self):
        """
        This method retrieves all buildings from the csv file and maps them to objects.
        Returns:
            buildings
        Return type:
            list[Building]
        """
        pass

    @abstractmethod
    def get_epw_pe_factors(self) -> List[PrimaryEnergyAndEmissionFactor]:
        """
        This method retrieves all primary energy and emission factors
        Returns:
            epw_pe_factors
        Return type:
            list[PrimaryEnergyAndEmissionFactor]
        """
        pass

    @abstractmethod
    def get_schedule(self, hk_geb: str, uk_geb: str) -> Union[Tuple[List[ScheduleName], str], HkOrUkNotFoundError]:
        """
        Find occupancy schedule from SIA2024, depending on hk_geb, uk_geb
        Args:
            hk_geb: Usage type (main category)
            uk_geb: Usage type (subcategory)

        Returns:
            schedule_name_list, schedule_name or throws an error
        Return type:
            Union[Tuple[List[ScheduleName], str], HkOrUkNotFoundError]
        """
        pass

    @abstractmethod
    def get_tek(self, hk_geb: str, uk_geb: str) -> Union[Tuple[float, str], ValueError]:
        """
        Find TEK values from Partial energy parameters to build the comparative values in accordance with the
        announcement  of 15.04.2021 on the Building Energy Act (GEG) of 2020, depending on hk_geb, uk_geb
        Args:
            hk_geb: Usage type (main category)
            uk_geb: Usage type (subcategory)

        Returns:
            tek_dhw, tek_name or throws an error
        Return type:
            Union[Tuple[float, str], ValueError]
        """
        pass

    @abstractmethod
    def get_weather_data(self, epw_file_path: str) -> List[WeatherData]:
        """
        This method read the file epw_file_path (csv or other extensions) and maps the result to objects
        Args:
            epw_file_path: file path

        Returns:
            weather_data_list
        Return type:
            List[WeatherData]
        """
        pass

    @abstractmethod
    def choose_and_get_the_right_weather_data_from_path(self, weather_period, file_name) -> List[WeatherData]:
        """
        This method retrieves the right weather data according to the given weather_period and file_name
        Args:
            weather_period: the period to simulate
            file_name: the file name to be read

        Returns:
            weather_data_objects
        Return type:
            List[WeatherData]
        """
        pass

    @abstractmethod
    def get_epw_file(self, plz: str, weather_period: str) -> EPWFile:
        """
        Function finds the epw file depending on building location, Pick latitude and longitude from plz_data and put
        values into a list and Calculate minimum distance to next weather station
        Args:
            plz: zipcode of the building
            weather_period: the period to simulate

        Returns:
            epw_file object
        Return type:
            EPWFile
        """
        pass

    @abstractmethod
    def get_usage_time(self, hk_geb: str, uk_geb: str, usage_from_norm: str) -> Union[Tuple[int, int], ValueError]:
        """
        Find building's usage time DIN 18599-10 or SIA2024
        Args:
            hk_geb: Usage type (main category)
            uk_geb: Usage type (subcategory)
            usage_from_norm: data source either 18599-10 or SIA2024

        Returns:
            usage_start, usage_end or throws error
        Return type:
            Union[Tuple[int, int], ValueError]
        """
        pass

    @abstractmethod
    def get_gains(self, hk_geb: str, uk_geb: str, profile_from_norm: str, gains_from_group_values: str) -> Tuple[
        Tuple[float, str], float]:
        """
        Find data from DIN V 18599-10 or SIA2024
        Args:
            hk_geb: Usage type (main category)
            uk_geb: Usage type (subcategory)
            profile_from_norm: data source either 18599-10 or SIA2024 [specified in model/all_building.py
            or model/simulator.py]
            gains_from_group_values: group in norm low/medium/high [specified in model/all_building.py
            or model/simulator.py]

        Returns:
            gain_person_and_typ_norm, appliance_gains
        Return type:
            Tuple[Tuple[float, str], float]
        """
        pass

    @abstractmethod
    def result_to_pandas_dataframe(self, result) -> pd.DataFrame:
        """
        Maps a list of objects to a pandas Dataframe
        Args:
            result: result of a simulated building

        Returns:
            dataframe
        Return type:
            pd.DataFrame

        """
        pass

    @abstractmethod
    def result_of_all_hours_to_excel(self, result, building):
        """
        Maps the results of the simulated building to an Excel file (all hours)
        Args:
            result: result
            building: the building to simulate

        Returns:
            Excel file
        Return type:
            None
        """
        pass

    @abstractmethod
    def build_all_results_of_all_buildings(self, results):
        """
        Converts the results of all buildings to an Excel file
        Args:
            results: results of all building

        Returns:
            Excel file
        Return type:
            None

        """
        pass
