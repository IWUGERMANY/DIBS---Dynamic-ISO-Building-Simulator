import os
from typing import List, Tuple, Union
import pandas as pd

from iso_simulator.data_source.datasource import DataSource

from iso_simulator.utils.utils_epwfile import get_coordinates_plz, get_weather_files_stations, \
    calculate_minimum_distance_to_next_weather_station, get_filename_with_minimum_distance, get_coordinates_station, \
    get_distance
from iso_simulator.utils.utils_normreader import find_row, get_value_error, get_usage_start_end, \
    get_gain_per_person_and_appliance_and_typ_norm_sia2024, get_gain_per_person_and_appliance_and_typ_norm_18599
from iso_simulator.utils.utils_readcsv import read_building_data, read_gwp_pe_factors_data, \
    read_occupancy_schedules_zuweisungen_data, read_schedule_file, read_vergleichswerte_zuweisung, \
    read_tek_nwg_vergleichswerte, read_weather_data, read_plz_codes_data, read_profiles_zuweisungen_data
from iso_simulator.utils.utils_hkgeb import hk_and_uk_in_zuweisungen, hk_or_uk_not_in_zuweisungen, hk_in_zuweisungen, \
    uk_in_zuweisungen
from iso_simulator.utils.utils_tekreader import get_tek_name, get_tek_data_frame_based_on_tek_name, get_tek_dhw
from iso_simulator.utils.utils_schedule import get_schedule_name, raise_exception

from iso_simulator.model.schedule_name import ScheduleName
from iso_simulator.model.building import Building
from iso_simulator.model.primary_energy_and_emission_factors import PrimaryEnergyAndEmissionFactor
from iso_simulator.model.weather_data import WeatherData
from iso_simulator.model.epw_file import EPWFile


class DataSourceCSV(DataSource):

    def get_building_data(self) -> Building:
        building_data: pd.DataFrame = read_building_data()
        return Building(*building_data.iloc[0].values)

    def get_epw_pe_factors(self) -> List[PrimaryEnergyAndEmissionFactor]:
        gwp_pe_factors: pd.DataFrame = read_gwp_pe_factors_data()

        return [
            PrimaryEnergyAndEmissionFactor(*row.values)
            for _, row in gwp_pe_factors.iterrows()
        ]

    def get_schedule(self, hk_geb: str, uk_geb: str) -> Union[Tuple[List[ScheduleName], str], ValueError]:
        zuweisungen: pd.DataFrame = read_occupancy_schedules_zuweisungen_data()

        if hk_and_uk_in_zuweisungen(zuweisungen, hk_geb, uk_geb):
            row: pd.DataFrame = find_row(zuweisungen, uk_geb)
            schedule_name: str = get_schedule_name(row)
            schedule_file: pd.DataFrame = read_schedule_file(schedule_name)

            return [
                ScheduleName(*row.values)
                for _, row in schedule_file.iterrows()
            ], schedule_name


        else:
            raise_exception('hk_geb')

    def get_schedule_sum(self, hk_geb: str, uk_geb: str) -> float:

        zuweisungen: pd.DataFrame = read_occupancy_schedules_zuweisungen_data()

        if hk_and_uk_in_zuweisungen(zuweisungen, hk_geb, uk_geb):
            row: pd.DataFrame = find_row(zuweisungen, uk_geb)
            schedule_name: str = get_schedule_name(row)
            schedule_file: pd.DataFrame = read_schedule_file(schedule_name)
            return schedule_file.People.sum()

    def get_tek(self, hk_geb: str, uk_geb: str) -> Union[Tuple[float, str], ValueError]:
        """
        Find TEK values from Teilenergiekennwerte zur Bildung der Vergleichswerte gemäß der Bekanntmachung vom 15.04.2021 zum Gebäudeenergiegesetz (GEG) vom 2020, 
        depending on hk_geb, uk_geb


        :external input data: ../auxiliary/TEKs/TEK_NWG_Vergleichswerte.csv


        :param hk_geb: usage type (main category)
        :type hk_geb: string
        :param uk_geb: usage type (subcategory)
        :type uk_geb: string

        :return: df_TEK, TEK_name
        :rtype: DataFrame (with floats), string
        """

        zuweisungen: pd.DataFrame = read_vergleichswerte_zuweisung()
        db_teks: pd.DataFrame = read_tek_nwg_vergleichswerte()

        if hk_or_uk_not_in_zuweisungen(zuweisungen, hk_geb, uk_geb):
            raise_exception('uk_geb or hk_geb')
        row: pd.DataFrame = find_row(zuweisungen, uk_geb)
        tek_name: str = get_tek_name(row)
        df_tek: pd.DataFrame = get_tek_data_frame_based_on_tek_name(db_teks, tek_name)
        tek_dhw: float = get_tek_dhw(df_tek)
        return tek_dhw, tek_name

    def get_weather_data(self, epwfile_path: str) -> List[WeatherData]:
        weather_data: pd.DataFrame = read_weather_data(epwfile_path)
        # .drop('datasource', axis=1)

        return [
            WeatherData(*row.values)
            for _, row in weather_data.iterrows()
        ]

    def choose_and_get_the_right_weather_data_from_path(self, weather_period, file_name) -> List[WeatherData]:
        return (
            self.get_weather_data(
                os.path.join(f'iso_simulator/auxiliary/weather_data/weather_data_TMYx_2007_2021{file_name}',
                             )
            )
            if weather_period == "2007-2021"
            else self.get_weather_data(
                os.path.join(
                    f'iso_simulator/auxiliary/weather_data/{file_name}')
            )
        )

    def get_epw_file(self, plz: str, weather_period: str) -> EPWFile:
        """
        Function finds the epw file depending on building location, Pick latitude and longitude from plz_data and put values into a list and 
        Calculate minimum distance to next weather station


        :external input data: File with german zip codes [../auxiliary/weather_data/plzcodes.csv]
                              File with metadata of weather stations (e.g. longitude, latitude) [../auxiliary/weather_data/weatherfiles_stations_93.csv]

        :return epw_filename: filename of the epw
        :rtype: tuple (string)
        :return coordinates_station: latitude and longitute of the selected station
        :rtype: tuple (float)
        """
        plz_data: pd.DataFrame = read_plz_codes_data()

        weatherfiles_stations: pd.DataFrame = get_weather_files_stations(
            weather_period)

        weatherfiles_stations['latitude_building'], weatherfiles_stations['longitude_building'] = get_coordinates_plz(
            plz_data, plz)

        calculate_minimum_distance_to_next_weather_station(weatherfiles_stations)

        epw_filename: str = get_filename_with_minimum_distance(
            weatherfiles_stations)

        coordinates_station: List = get_coordinates_station(
            weatherfiles_stations)

        distance: float = get_distance(weatherfiles_stations)

        return EPWFile(epw_filename, coordinates_station, distance)

    def get_usage_time(self, hk_geb: str, uk_geb: str, usage_from_norm: str) -> Union[Tuple[int, int], ValueError]:

        gains_zuweisungen: pd.DataFrame = read_profiles_zuweisungen_data()

        if hk_in_zuweisungen(hk_geb, gains_zuweisungen):

            if not uk_in_zuweisungen(uk_geb, gains_zuweisungen):
                get_value_error()

            row: pd.DataFrame = find_row(gains_zuweisungen, uk_geb)

            return get_usage_start_end(usage_from_norm, row)

    def get_gains(self, hk_geb: str, uk_geb: str, profile_from_norm, gains_from_group_values) -> Tuple[
        Tuple[float, str], float]:
        """
        Find data from DIN V 18599-10 or SIA2024


        :external input data: Assignments [../auxiliary/norm_profiles/profiles_zuweisungen.csv]

        :param hk_geb: usage type (main category)
        :type hk_geb: string
        :param uk_geb: usage type (subcategory)
        :type uk_geb: string
        :param profile_from_norm: data source either 18599-10 or SIA2024 [specified in annualSimulation.py]
        :type profile_from_norm: string
        :param gains_from_group_values: group in norm low/medium/high [specified in annualSimulation.py]
        :type gains_from_group_values: string

        :return: gain_per_person, appliance_gains, typ_norm
        :rtype: tuple (float, float, string)
        """

        gains_zuweisungen: pd.DataFrame = read_profiles_zuweisungen_data()

        if hk_and_uk_in_zuweisungen(gains_zuweisungen, hk_geb, uk_geb):
            row: pd.DataFrame = find_row(gains_zuweisungen, uk_geb)

            gain_person_and_typ_norm: Tuple[float, str]
            appliance_gains: float

            if profile_from_norm == 'sia2024':
                gain_person_and_typ_norm, appliance_gains = get_gain_per_person_and_appliance_and_typ_norm_sia2024(
                    gains_from_group_values, row)

            else:
                gain_person_and_typ_norm, appliance_gains = get_gain_per_person_and_appliance_and_typ_norm_18599(
                    row, gains_from_group_values)

        return gain_person_and_typ_norm, appliance_gains
