"""
This class is responsible for generating the input data only once to avoid generating after each building simulation.
"""

from iso_simulator.data_source.datasource_csv import DataSourceCSV
from iso_simulator.model.building import Building
from iso_simulator.model.primary_energy_and_emission_factors import PrimaryEnergyAndEmissionFactor
from typing import List


class GenerateData:

    def __init__(self, datasource: DataSourceCSV, weather_period: str):
        """
        This constructor to initialize an instance of the GenerateData class
        Args:
            datasource: where the implementation of the methods for processing data are
            weather_period: the period to simulate
        """
        self.datasource = datasource
        self.weather_period = weather_period
        self.all_buildings = self.get_all_buildings()
        self.gwp_PE_Factors = datasource.get_epw_pe_factors()

    def get_all_buildings(self) -> List[Building]:
        """
        Retrieve all building
        Returns:
            all_building
        Return type:
            list[Building]
        """
        return self.datasource.get_all_buildings()

    def get_epw_pe_factors(self) -> List[PrimaryEnergyAndEmissionFactor]:
        """
        Retrieve all epw_pe_factors
        Returns:
            epw_pe_factors
        Return type:
            list[PrimaryEnergyAndEmissionFactor]
        """
        return self.datasource.get_epw_pe_factors()

    def filter_building_by_src_id(self, building_id: str) -> Building:
        """
        Look up the building with the given building_id
        Args:
            building_id: the id of the building that the user wants to simulate
        Returns:
            building
        Return type:
            Building
        """
        for building in self.all_buildings:
            if building.scr_gebaeude_id == building_id:
                return building

    def filter_list(self, building_id: str):
        my_filter = filter(lambda x: (x.scr_gebaeude_id == building_id), self.all_buildings)
        return my_filter
