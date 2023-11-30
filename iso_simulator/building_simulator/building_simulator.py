from iso_simulator.model import window
from iso_simulator.model.location import Location
from iso_simulator.model.schedule_name import ScheduleName
from iso_simulator.model.weather_data import WeatherData
from iso_simulator.model.results import Result
from iso_simulator.model.window import Window

from iso_simulator.data_source.datasource_csv import DataSourceCSV

from iso_simulator.utils.utils_methods import *

from typing import List, Tuple, Union
import pandas as pd
import time


__author__ = "Wail Samjouni"
__copyright__ = "Copyright 2023, Institut Wohnen und Umwelt"
__license__ = "MIT"


class BuildingSimulator:

    def __init__(self,
                 datasourcecsv: DataSourceCSV,
                 weather_period: str,
                 profile_from_norm: str,
                 gains_from_group_values: str
                 ):
        self.datasourcecsv = datasourcecsv
        self.weather_period = weather_period
        self.building_object = datasourcecsv.get_building_data()
        self.gwp_PE_Factors = datasourcecsv.get_epw_pe_factors()
        self.epw_object = datasourcecsv.get_epw_file(
            self.building_object.plz, self.weather_period)
        self.result = Result()
        self.profile_from_norm = profile_from_norm
        self.gains_from_group_values = gains_from_group_values
        self.all_windows = self.build_windows_objects()

    def initialize_building_time(self) -> float:
        return time.time()

    def calculate_building_time(self) -> float:
        return time.time() - self.initialize_building_time()

    def check_energy_area_and_heating(self) -> None:
        check_energy_ref_area = self.building_object.energy_ref_area == -8
        check_heating_supply_system = self.building_object.heating_supply_system == 'NoHeating'
        if check_energy_ref_area or check_heating_supply_system:
            print(
                f'Building {str(self.building_object.scr_gebaeude_id)} not heated')

    # def build_south_window(self) -> Window:
    #     return Window(0, self.building_object.glass_solar_transmittance, self.building_object.glass_solar_shading_transmittance,
    #                   self.building_object.glass_light_transmittance, self.building_object.window_area_south)

    # def build_east_window(self) -> Window:
    #     return Window(90,
    #                   self.building_object.glass_solar_transmittance, self.building_object.glass_solar_shading_transmittance,
    #                   self.building_object.glass_light_transmittance, self.building_object.window_area_east)

    # def build_west_window(self) -> Window:
    #     return Window(180, self.building_object.glass_solar_transmittance, self.building_object.glass_solar_shading_transmittance,
    #                   self.building_object.glass_light_transmittance, self.building_object.window_area_west)

    # def build_north_window(self) -> Window:
    #     return Window(270, self.building_object.glass_solar_transmittance, self.building_object.glass_solar_shading_transmittance,
    #                   self.building_object.glass_light_transmittance, self.building_object.window_area_north)

    def build_south_window(self) -> Window:
        return Window(azimuth_tilt=0, alititude_tilt=90,
                      glass_solar_transmittance=self.building_object.glass_solar_transmittance,
                      glass_solar_shading_transmittance=self.building_object.glass_solar_shading_transmittance,
                      glass_light_transmittance=self.building_object.glass_light_transmittance,
                      area=self.building_object.window_area_south)

    def build_east_window(self) -> Window:
        return Window(azimuth_tilt=90, alititude_tilt=90,
                      glass_solar_transmittance=self.building_object.glass_solar_transmittance,
                      glass_solar_shading_transmittance=self.building_object.glass_solar_shading_transmittance,
                      glass_light_transmittance=self.building_object.glass_light_transmittance,
                      area=self.building_object.window_area_east)

    def build_west_window(self) -> Window:
        return Window(azimuth_tilt=180, alititude_tilt=90,
                      glass_solar_transmittance=self.building_object.glass_solar_transmittance,
                      glass_solar_shading_transmittance=self.building_object.glass_solar_shading_transmittance,
                      glass_light_transmittance=self.building_object.glass_light_transmittance,
                      area=self.building_object.window_area_west)

    def build_north_window(self) -> Window:
        return Window(azimuth_tilt=270, alititude_tilt=90,
                      glass_solar_transmittance=self.building_object.glass_solar_transmittance,
                      glass_solar_shading_transmittance=self.building_object.glass_solar_shading_transmittance,
                      glass_light_transmittance=self.building_object.glass_light_transmittance,
                      area=self.building_object.window_area_north)

    def build_windows_objects(self) -> List[Window]:
        return [
            self.build_south_window(),
            self.build_east_window(),
            self.build_west_window(),
            self.build_north_window()
        ]

    def get_usage_start_and_end(self) -> Tuple[int, int]:
        usage_start, usage_end = self.datasourcecsv.get_usage_time(
            self.building_object.hk_geb, self.building_object.uk_geb, self.profile_from_norm)
        return usage_start, usage_end

    def get_schedule(self) -> Union[Tuple[List[ScheduleName], str], ValueError]:
        return self.datasourcecsv.get_schedule(
            self.building_object.hk_geb, self.building_object.uk_geb)

    def get_tek(self) -> Union[Tuple[float, str], ValueError]:
        return self.datasourcecsv.get_tek(self.building_object.hk_geb, self.building_object.uk_geb)

    # def get_occupancy_full_usage_hours(self, occupancy_schedule: List[ScheduleName]) -> float:
    #     # return sum(schedule.People for schedule in occupancy_schedule)

    def get_occupancy_full_usage_hours(self) -> float:
        return self.datasourcecsv.get_schedule_sum(self.building_object.hk_geb, self.building_object.uk_geb)


# ----------------------------------------------------------------

    def get_weather_data(self) -> List[WeatherData]:
        epw_object = self.datasourcecsv.get_epw_file(
            self.building_object.plz, self.weather_period)
        return self.datasourcecsv.choose_and_get_the_right_weather_data_from_path(self.weather_period, epw_object.file_name)

    def extract_outdoor_temperature(self, weather_data: List[WeatherData], hour: int) -> float:
        """
        Extract the outdoor temperature in building_location for that hour from weather_data
        """
        return weather_data[hour].drybulb_C

    def extract_year(self, weather_data: List[WeatherData], hour: int) -> int:
        return weather_data[hour].year

    def get_altitude_and_zimuth(self, hour: int) -> Tuple[float, float]:
        location = Location()
        epw_file = self.datasourcecsv.get_epw_file(
            self.building_object.plz, self.weather_period)
        weather_data = self.datasourcecsv.choose_and_get_the_right_weather_data_from_path(
            self.weather_period, epw_file.file_name)
        return location.calc_sun_position(
            epw_file.coordinates_station[0], epw_file.coordinates_station[1], self.extract_year(weather_data, hour), hour)

    def calc_building_h_ve_adj(self, hour: int, t_out: float, usage_start: int, usage_end: int) -> float:
        return self.building_object.calc_h_ve_adj(hour, t_out, usage_start, usage_end)

    def set_t_air_based_on_hour(self, hour) -> float:
        t_air = self.building_object.t_set_heating if hour == 0 else self.building_object.t_air
        return t_air

    def calc_solar_gains_for_all_windows(self, weather_data: List[WeatherData], sun_altitude: float, sun_azimuth: float, t_air: float, hour: int):

        for element in self.all_windows:
            element.calc_solar_gains(
                sun_altitude, sun_azimuth, weather_data[hour].dirnorrad_Whm2, weather_data[hour].difhorrad_Whm2, t_air, hour)

    def calc_illuminance_for_all_windows(self, weather_data: List[WeatherData], sun_altitude: float, sun_azimuth: float, t_air: float, hour: int):

        for element in self.all_windows:
            element.calc_illuminance(
                sun_altitude, sun_azimuth, weather_data[hour].dirnorillum_lux, weather_data[hour].difhorillum_lux)
