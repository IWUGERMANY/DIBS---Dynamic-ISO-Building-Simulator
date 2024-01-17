"""
This class is responsible for generating the input data only once to avoid generating after each building simulation.
"""

from iso_simulator.data_source.datasource_csv import DataSourceCSV
from iso_simulator.model.building import Building
from iso_simulator.model.primary_energy_and_emission_factors import PrimaryEnergyAndEmissionFactor
from typing import List


class GenerateData:

    def __init__(self, datasource: DataSourceCSV):
        """
        This constructor to initialize an instance of the GenerateData class
        Args:
            datasource: where the implementation of the methods for processing data are
            weather_period: the period to simulate
        """
        self.datasource = datasource
        self.all_buildings = self.get_all_buildings()
        self.gwp_pe_factors = datasource.get_epw_pe_factors()

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

    def filter_list(self, building_id: str):
        building = next((building for building in self.all_buildings if building.scr_gebaeude_id == building_id), None)
        return building
