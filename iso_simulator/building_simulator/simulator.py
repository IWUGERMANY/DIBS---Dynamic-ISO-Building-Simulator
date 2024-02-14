"""
this class implements the business logic to simulate a given building
"""

from iso_simulator.model.calculations_sum import CalculationOfSum
from iso_simulator.model.location import Location
from iso_simulator.model.schedule_name import ScheduleName
from iso_simulator.model.weather_data import WeatherData
from iso_simulator.model.results import Result
from iso_simulator.model.window import Window
from iso_simulator.data_source.datasource_csv import DataSourceCSV
from iso_simulator.exceptions.ghg_emission import GHGEmissionError
from iso_simulator.exceptions.building_not_heated_exception import (
    BuildingNotHeatedError,
)

from typing import List, Tuple, Union
import time

__author__ = "Wail Samjouni"
__copyright__ = "Copyright 2023, Institut Wohnen und Umwelt"
__license__ = "MIT"


class BuildingSimulator:
    def __init__(
            self,
            path: str,
            datasource: DataSourceCSV,
            weather_period: str,
            profile_from_norm: str,
            gains_from_group_values: str,
            usage_from_norm: str,
    ):
        """
        This constructor to initialize an instance of the BuildingSimulator class
        Args:
            datasource: object contains implemented methods of DataSource interface
            all_building: object contains all buildings
            building_by_id: building with a specific id (to simulate)
            gwp_PE_Factors: all primary energy and emission factors
            weather_period: period to simulate
            profile_from_norm: data source either 18599-10 or SIA2024
            gains_from_group_values: group in norm low/medium/high
            usage_from_norm: data source either 18599-10 or SIA2024
        """
        self.datasource = datasource
        self.weather_period = weather_period
        self.building_object = self.datasource.get_user_building(path)
        self.gwp_PE_Factors = self.datasource.get_epw_pe_factors()
        self.epw_object = datasource.get_epw_file(
            self.building_object.plz, self.weather_period
        )
        self.result = Result()
        self.profile_from_norm = profile_from_norm
        self.gains_from_group_values = gains_from_group_values
        self.usage_from_norm = usage_from_norm
        self.all_windows = self.build_windows_objects()
        self.weather_data = self.get_weather_data()

    def initialize_building_time(self) -> float:
        return time.time()

    def calculate_building_time(self) -> float:
        return time.time() - self.initialize_building_time()

    def check_energy_area_and_heating(self):
        """
        If there's no heated area (energy_ref_area == -8) or no heating supply system (heating_supply_system == 'NoHeating')
        no heating demand can be calculated. In this case skip calculation and proceed with next building.
        Returns:

        """
        check_energy_ref_area = self.building_object.energy_ref_area == -8
        check_heating_supply_system = (
                self.building_object.heating_supply_system == "NoHeating"
        )
        try:
            if check_energy_ref_area or check_heating_supply_system:
                raise BuildingNotHeatedError(
                    f"Building {str(self.building_object.scr_gebaeude_id)} not heated"
                )
        except BuildingNotHeatedError as error:
            print(error)

    def build_south_window(self) -> Window:
        """
        This method builds a window object
        Returns:
            window
        Return type
            Window
        """
        return Window(
            0,
            90,
            self.building_object.glass_solar_transmittance,
            self.building_object.glass_solar_shading_transmittance,
            self.building_object.glass_light_transmittance,
            self.building_object.window_area_south,
        )

    def build_east_window(self) -> Window:
        """
        This method builds a window object
        Returns:
            window
        Return type
            Window
        """

        return Window(
            90,
            90,
            self.building_object.glass_solar_transmittance,
            self.building_object.glass_solar_shading_transmittance,
            self.building_object.glass_light_transmittance,
            self.building_object.window_area_east,
        )

    def build_west_window(self) -> Window:
        """
        This method builds a window object
       Returns:
            window
        Return type
            Window
        """
        return Window(
            180,
            90,
            self.building_object.glass_solar_transmittance,
            self.building_object.glass_solar_shading_transmittance,
            self.building_object.glass_light_transmittance,
            self.building_object.window_area_west,
        )

    def build_north_window(self) -> Window:
        """
        This method builds a window object
        Returns:
            window
        Return type
            Window
        """
        return Window(
            270,
            90,
            self.building_object.glass_solar_transmittance,
            self.building_object.glass_solar_shading_transmittance,
            self.building_object.glass_light_transmittance,
            self.building_object.window_area_north,
        )

    def build_windows_objects(self) -> List[Window]:
        """
        This method builds a list of all windows (south, west, east and north)
        Returns:
            windows
        Return type
            List[Window]
        """
        return [
            self.build_south_window(),
            self.build_east_window(),
            self.build_west_window(),
            self.build_north_window(),
        ]

    def get_usage_start_and_end(self) -> Tuple[int, int]:
        """
        Find building's usage time DIN 18599-10 or SIA2024
        Returns:
            usage_start, usage_end
        Return type
            Tuple[int, int]
        """
        usage_start, usage_end = self.datasource.get_usage_time(
            self.building_object.hk_geb,
            self.building_object.uk_geb,
            self.usage_from_norm,
        )
        return usage_start, usage_end

    def get_schedule(self) -> Union[Tuple[List[ScheduleName], str, float], ValueError]:
        """
        Find occupancy schedule from SIA2024, depending on hk_geb, uk_geb from csv file
        Returns:
            list_of_schedule_name, schedule_name or throws an error
        Return type
            Union[Tuple[List[ScheduleName], str, float], ValueError]
        """
        return self.datasource.get_schedule(
            self.building_object.hk_geb, self.building_object.uk_geb
        )

    def get_tek(self) -> Union[Tuple[float, str], ValueError]:
        """
        Find TEK values from Partial energy parameters to build the comparative values in accordance with the
        announcement  of 15.04.2021 on the Building Energy Act (GEG) of 2020, depending on hk_geb, uk_geb
        Returns:
            tek_dhw, tek_name or throws an error
        Return type
            Union[Tuple[float, str], ValueError]
        """
        return self.datasource.get_tek(
            self.building_object.hk_geb, self.building_object.uk_geb
        )

    # def get_occupancy_full_usage_hours(self) -> float:
    #
    #     return self.datasourcecsv.get_schedule_sum(self.building_object.hk_geb, self.building_object.uk_geb)

    def get_weather_data(self) -> List[WeatherData]:
        """
        This method retrieves the right weather data according to the given weather_period and file_name

        Returns:
            weather_data_objects
        Return type
            List[WeatherData]
        """
        return self.datasource.choose_and_get_the_right_weather_data_from_path(
            self.weather_period, self.epw_object.file_name
        )

    def extract_outdoor_temperature(self, hour: int) -> float:
        """
        Extract the outdoor temperature in building_location for that hour from weather_data
        Args:
            hour: hour to simulate

        Returns:
            outdoor_temperature
        Return type
            float
        """
        return self.weather_data[hour].drybulb_C

    def extract_year(self, hour: int) -> int:
        """
        Extract the year based on a given hour
        Args:
            hour: hour to simulate

        Returns:
            year
        Return type
            int
        """
        return self.weather_data[hour].year

    def calc_altitude_and_azimuth(self, hour: int) -> Tuple[float, float]:
        """
        Call calc_sun_position(). Depending on latitude, longitude, year and hour - Independent from epw weather_data
        Args:
            hour: hour to simulate

        Returns:
            altitude, azimuth
        Return type
            Tuple[float, float]
        """
        location = Location()
        return location.calc_sun_position(
            self.epw_object.coordinates_station[0],
            self.epw_object.coordinates_station[1],
            self.extract_year(hour),
            hour,
        )

    def calc_building_h_ve_adj(
            self, hour: int, t_out: float, usage_start: int, usage_end: int
    ) -> float:
        """
        Calculate H_ve_adj, See building_physics for details
        Args:
            hour: hour to simulate
            t_out: Outdoor air temperature [C]
            usage_start: Beginning of usage time according to SIA2024
            usage_end: Ending of usage time according to SIA2024

        Returns:
            h_ve_adj
        Return type
            float
        """
        return self.building_object.calc_h_ve_adj(hour, t_out, usage_start, usage_end)

    def set_t_air_based_on_hour(self, hour: int) -> float:
        """
         Define t_air for calc_solar_gains(). Starting condition (hour==0) necessary for first time step
        Args:
            hour: hour to simulate

        Returns:
            t_air
        Return type
            float

        """
        t_air = (
            self.building_object.t_set_heating
            if hour == 0
            else self.building_object.t_air
        )
        return round(t_air, 2)

    def calc_solar_gains_for_all_windows(
            self, sun_altitude: float, sun_azimuth: float, t_air: float, hour: int
    ) -> None:
        """
        Calculates the solar gains in the building zone through the set window
        Args:
            sun_altitude: Altitude Angle of the Sun in Degrees
            sun_azimuth: Azimuth angle of the sun in degrees
            t_air:
            hour: hour to simulate

        Return type:
            None

        """

        for element in self.all_windows:
            element.calc_solar_gains(
                sun_altitude,
                sun_azimuth,
                self.weather_data[hour].dirnorrad_Whm2,
                self.weather_data[hour].difhorrad_Whm2,
                t_air,
                hour,
            )

    def calc_illuminance_for_all_windows(
            self, sun_altitude: float, sun_azimuth: float, hour: int
    ) -> None:
        """
        Calculates the illuminance in the building zone through the set window
        Args:
            sun_altitude: Altitude Angle of the Sun in Degrees
            sun_azimuth: Azimuth angle of the sun in degrees
            hour: hour to simulate

        Return type:
            None

        """

        for element in self.all_windows:
            element.calc_illuminance(
                sun_altitude,
                sun_azimuth,
                self.weather_data[hour].dirnorillum_lux,
                self.weather_data[hour].difhorillum_lux,
            )

    def calc_occupancy(
            self, occupancy_schedule: List[ScheduleName], hour: int
    ) -> float:
        """
        Calc occupancy for the time step
        Args:
            occupancy_schedule: schedule name
            hour: hour to simulate

        Returns:
            occupancy
        Return type
            float

        """
        return occupancy_schedule[hour].People * self.building_object.max_occupancy

    def calc_sum_illuminance_all_windows(self) -> float:
        """
        Sum of transmitted illuminance of all windows
        Returns:
            transmitted illuminance_sum
        Return type
            float

        """
        return sum(element.transmitted_illuminance for element in self.all_windows)

    def solve_building_lightning(self, occupancy_percent: float) -> None:
        """
        Calculate the lighting of the building for the time step
        Args:
            occupancy_percent: occupancy for the time step

        Return type:
            None

        """
        self.building_object.solve_building_lighting(
            self.calc_sum_illuminance_all_windows(), occupancy_percent
        )

    def calc_gains_from_occupancy_and_appliances(
            self,
            occupancy_schedule: List[ScheduleName],
            occupancy: float,
            gain_per_person: float,
            appliance_gains: float,
            hour: int,
    ) -> float:
        """
        Calculate gains from occupancy and appliances
        This is thermal gains. Negative appliance_gains are heat sinks!
        Args:
            occupancy_schedule: schedule name
            occupancy: Occupancy [people]
            gain_per_person:
            appliance_gains:
            hour: hour to simulate

        Returns:
            internal_gains
        Return type
            float

        """
        return (
                occupancy * gain_per_person
                + appliance_gains
                * occupancy_schedule[hour].Appliances
                * self.building_object.energy_ref_area
                + self.building_object.lighting_demand
        )

    def calc_appliance_gains_demand(
            self, occupancy_schedule: List[ScheduleName], appliance_gains: float, hour: int
    ) -> float:
        """
        Calculate appliance_gains as part of the internal_gains
        Args:
            occupancy_schedule: schedule name
            appliance_gains:
            hour: hour to simulate

        Returns:
            appliance_gains_demand
        Return type
            float

        """
        return (
                appliance_gains
                * occupancy_schedule[hour].Appliances
                * self.building_object.energy_ref_area
        )

    def get_appliance_gains_elt_demand(
            self, occupancy_schedule: List[ScheduleName], appliance_gains: float, hour: int
    ) -> float:
        """
        Appliance_gains equal the electric energy that appliances use, except for negative appliance_gains of refrigerated counters in trade buildings for food!
        The assumption is: negative appliance_gains come from referigerated counters with heat pumps for which we assume a COP = 2.
        Args:
            occupancy_schedule: schedule name
            appliance_gains:
            hour: hour to simulate

        Returns:
            appliance_gains_elt_demand
        Return type
            float

        """
        appliance_gains_elt = (
            -1 * appliance_gains / 2 if appliance_gains < 0 else appliance_gains
        )
        return (
                appliance_gains_elt
                * occupancy_schedule[hour].Appliances
                * self.building_object.energy_ref_area
        )

    def calc_sum_solar_gains_all_windows(self) -> float:
        """
        Sum of solar gains of all windows
        Returns:
            solar_gains_sum
        Return type
            float

        """
        return sum(element.solar_gains for element in self.all_windows)

    def calc_energy_demand_for_time_step(
            self, internal_gains: float, t_out: float, t_m_prev: float
    ) -> None:
        """
        Calculate energy demand for the time step
        Args:
            internal_gains: internal heat gains from people and appliances [W]
            t_out: Outdoor temperature of this timestep
            t_m_prev:  Previous air temperature [C]

        Return type:
            None

        """
        self.building_object.solve_building_energy(
            internal_gains, self.calc_sum_solar_gains_all_windows(), t_out, t_m_prev
        )

    def check_if_central_heating_or_central_dhw(self) -> bool:
        """
        Checks if dhw system of the building in the list named central
        Returns:
            True or False
        Return typ
            boolean

        """
        central = ["CentralHeating", "CentralDHW"]
        return self.building_object.dhw_system in central

    def check_if_heat_pump_air_or_ground_source(self) -> bool:
        """
        Checks if dhw system of the building in the list named heat_source
        Returns:
            True or False
        Return typ
            boolean

        """
        heat_source = ["HeatPumpAirSource", "HeatPumpGroundSource", "ElectricHeating"]
        return self.building_object.heating_supply_system in heat_source

    def calc_hot_water_usage(
            self,
            occupancy_schedule: List[ScheduleName],
            tek_dhw_per_occupancy_full_usage_hour: float,
            hour: int,
    ) -> Tuple[float, float, float, float]:
        """
        Calculate hot water usage of the building for the time step with (self.building_object.heating_energy /
        self.building_object.heating_demand)
        represents the Efficiency of the heat generation in the building
        Args:
            occupancy_schedule:
            tek_dhw_per_occupancy_full_usage_hour:
            hour:

        Returns:
            hot_water_demand, hot_water_energy, hot_water_sys_electricity, hot_water_sys_fossils
        Return type
            Tuple[float, float, float, float]

        """
        if self.building_object.dhw_system not in ["NoDHW", " -"]:
            hot_water_demand = (
                    occupancy_schedule[hour].People
                    * tek_dhw_per_occupancy_full_usage_hour
                    * 1000
                    * self.building_object.energy_ref_area
            )

            if self.building_object.heating_demand > 0:
                hot_water_energy = hot_water_demand * (
                        self.building_object.heating_energy
                        / self.building_object.heating_demand
                )
            else:
                hot_water_energy = hot_water_demand

            if self.building_object.dhw_system == "DecentralElectricDHW" or (
                    self.check_if_central_heating_or_central_dhw()
                    and self.check_if_heat_pump_air_or_ground_source()
            ):
                hot_water_sys_electricity = hot_water_energy
                hot_water_sys_fossils = 0
            else:
                hot_water_sys_fossils = hot_water_energy
                hot_water_sys_electricity = 0
        else:
            hot_water_demand = 0
            hot_water_energy = 0
            hot_water_sys_electricity = 0
            hot_water_sys_fossils = 0

        return (
            hot_water_demand,
            hot_water_energy,
            hot_water_sys_electricity,
            hot_water_sys_fossils,
        )

    def biogas_boiler_types(self) -> bool:
        """
        Checks if heating supply system of the building in the list named biogas_boiler_types
        Returns:
            True or False
        Return typ
            boolean
        """

        biogas_boiler_types = [
            "BiogasBoilerCondensingBefore95",
            "BiogasBoilerCondensingFrom95",
        ]
        return self.building_object.heating_supply_system in biogas_boiler_types

    def biogas_oil_boilers_types(self) -> bool:
        """
        Checks if heating supply system of the building in the list named biogas_oil_boilers_types
        Returns:
            True or False
        Return typ
            boolean

        """
        biogas_oil_boilers_types = [
            "BiogasOilBoilerLowTempBefore95",
            "BiogasOilBoilerCondensingFrom95",
            "BiogasOilBoilerCondensingImproved",
        ]
        return self.building_object.heating_supply_system in biogas_oil_boilers_types

    def oil_boiler_types(self) -> bool:
        """
        Checks if heating supply system of the building in the list named oil_boiler_types
        Returns:
            True or False
        Return typ
            boolean

        """
        oil_boiler_types = [
            "OilBoilerStandardBefore86",
            "OilBoilerStandardFrom95",
            "OilBoilerLowTempBefore87",
            "OilBoilerLowTempBefore95",
            "OilBoilerLowTempFrom95",
            "OilBoilerCondensingBefore95",
            "OilBoilerCondensingFrom95",
            "OilBoilerCondensingImproved",
        ]
        return self.building_object.heating_supply_system in oil_boiler_types

    def lgas_boiler_temp(self) -> bool:
        """
        Checks if heating supply system of the building in the list named lgas_boiler_temp
        Returns:
            True or False
        Return typ
            boolean

        """
        lgas_boiler_temp = [
            "LGasBoilerLowTempBefore95",
            "LGasBoilerLowTempFrom95",
            "LGasBoilerCondensingBefore95",
            "LGasBoilerCondensingFrom95",
            "LGasBoilerCondensingImproved",
            "LGasBoilerLowTempBefore87",
        ]
        return self.building_object.heating_supply_system in lgas_boiler_temp

    def gas_boiler_standard(self) -> bool:
        """
        Checks if heating supply system of the building in the list named gas_boiler_standard
        Returns:
            True or False
        Return typ
            boolean

        """
        gas_boiler_standard = [
            "GasBoilerStandardBefore86",
            "GasBoilerStandardBefore95",
            "GasBoilerStandardFrom95",
            "GasBoilerLowTempBefore87",
            "GasBoilerLowTempBefore95",
            "GasBoilerLowTempFrom95",
            "GasBoilerLowTempSpecialFrom78",
            "GasBoilerLowTempSpecialFrom95",
            "GasBoilerCondensingBefore95",
            "GasBoilerCondensingImproved",
            "GasBoilerCondensingFrom95",
        ]
        return self.building_object.heating_supply_system in gas_boiler_standard

    def coal_solid_fuel_boiler(self) -> bool:
        """
        Checks if heating supply system of the building is CoalSolidFuelBoiler
        Returns:
            True or False
        Return typ
            boolean

        """
        return self.building_object.heating_supply_system == "CoalSolidFuelBoiler"

    def solid_fuel_liquid_fuel_furnace(self) -> bool:
        """
        Checks if heating supply system of the building is SolidFuelLiquidFuelFurnace
        Returns:
            True or False
        Return typ
            boolean

        """
        return (
                self.building_object.heating_supply_system == "SolidFuelLiquidFuelFurnace"
        )

    def heat_pump(self) -> bool:
        """
        Checks if heating supply system of the building in the list named heat_pumping
        Returns:
            True or False
        Return typ
            boolean

        """
        heat_pumping = ["HeatPumpAirSource", "HeatPumpGroundSource"]
        return self.building_object.heating_supply_system in heat_pumping

    def wood(self) -> bool:
        """
        Checks if heating supply system of the building in the list named wood
        Returns:
            True or False
        Return typ
            boolean

        """
        wood = [
            "WoodChipSolidFuelBoiler",
            "WoodPelletSolidFuelBoiler",
            "WoodSolidFuelBoilerCentral",
        ]
        return self.building_object.heating_supply_system in wood

    def gas_chip(self) -> bool:
        """
        Checks if heating supply system of the building is GasCHP
        Returns:
            True or False
        Return typ
            boolean

        """
        return self.building_object.heating_supply_system == "GasCHP"

    def district_heating(self) -> bool:
        """
        Checks if heating supply system of the building is DistrictHeating
        Returns:
            True or False
        Return typ
            boolean

        """
        return self.building_object.heating_supply_system == "DistrictHeating"

    def electric_heating(self) -> bool:
        """
        Checks if heating supply system of the building is ElectricHeating
        Returns:
            True or False
        Return typ
            boolean

        """
        return self.building_object.heating_supply_system == "ElectricHeating"

    def direct_heater(self) -> bool:
        """
        Checks if heating supply system of the building is DirectHeater
        Returns:
            True or False
        Return typ
            boolean

        """
        return self.building_object.heating_supply_system == "DirectHeater"

    def no_heating(self) -> bool:
        """
        Checks if heating supply system of the building is NoHeating
        Returns:
            True or False
        Return typ
            boolean

        """
        return self.building_object.heating_supply_system == "NoHeating"

    def first_natural_gas(self) -> bool:
        """
        Checks if heating supply system of the building in the list named lgaz
        Returns:
            True or False
        Return typ
            boolean

        """
        lgaz = [
            "LGasBoilerLowTempBefore95",
            "LGasBoilerLowTempFrom95",
            "LGasBoilerCondensingBefore95",
            "LGasBoilerCondensingFrom95",
            "LGasBoilerCondensingImproved",
            "LGasBoilerLowTempBefore87",
        ]
        return self.building_object.heating_supply_system in lgaz

    def heat_pump_or_electric_heating(self) -> bool:
        """
        See above method heat_pump() and electric_heating() for more information
        Returns:
            True or False
        Return type
            bool

        """
        return self.heat_pump() | self.electric_heating()

    def hard_coal(self) -> bool:
        """
        See above method coal_solid_fuel_boiler() and solid_fuel_liquid_fuel_furnace() for more information
        Returns:
            True or False
        Return type
            bool

        """
        return self.coal_solid_fuel_boiler() or self.solid_fuel_liquid_fuel_furnace()

    def choose_the_fuel_type(self) -> str:
        """
        Choose the fuel type based on the heating_supply_system of the building
        Returns:
            fuel_type
        Return type
            str
        """
        try:
            if self.biogas_boiler_types():
                return "Biogas (general)"
            elif self.biogas_oil_boilers_types():
                return "Biogas Bio-oil Mix (general)"
            elif self.oil_boiler_types():
                return "Light fuel oil"
            elif self.first_natural_gas():
                return "Natural gas"
            elif self.gas_boiler_standard():
                return "Natural gas"
            elif self.wood():
                return "Wood"
            elif self.coal_solid_fuel_boiler():
                return "Hard coal"
            elif self.solid_fuel_liquid_fuel_furnace():
                return "Hard coal"
            elif self.heat_pump():
                return "Electricity grid mix"
            elif self.gas_chip():
                return "Natural gas"
            elif self.district_heating():
                return "District heating (Combined Heat and Power) Gas or Liquid fuels"
            elif self.electric_heating():
                return "Electricity grid mix"
            elif self.direct_heater():
                return "District heating (Combined Heat and Power) Coal"
            elif self.no_heating():
                return "None"
            else:
                raise GHGEmissionError(
                    "Error occured during calculation of GHG-Emission for Heating. The following heating_supply_system cannot be considered yet"
                )
        except GHGEmissionError as error:
            print(error)

    def get_ghg_factor_heating(self, fuel_type: str):
        """
        GHG-Factor Heating
        Args:
            fuel_type: fuel_type

        Returns:
            gwp_specific_to_heating_value_GEG
        """

        filtered_list = [
            gwp_PE_Factor.gwp_spezific_to_heating_value_GEG
            for gwp_PE_Factor in self.gwp_PE_Factors
            if gwp_PE_Factor.energy_carrier == fuel_type
        ]
        return filtered_list[0] if filtered_list else None

    def get_pe_factor_heating(self, fuel_type: str):
        """
        PE-Factor Heating
        Args:
            fuel_type: fuel_type

        Returns:
            primary_energy_factor_GEG
        """

        filtered_list = [
            gwp_PE_Factor.primary_energy_factor_GEG
            for gwp_PE_Factor in self.gwp_PE_Factors
            if gwp_PE_Factor.energy_carrier == fuel_type
        ]
        return filtered_list[0] if filtered_list else None

    def get_conversion_factor_heating(self, fuel_type: str):
        """
        Umrechnungsfaktor von Brennwert (Hs) zu Heizwert (Hi) einlesen
        Args:
            fuel_type: fuel_type

        Returns:
            relation_calorific_to_heating_value_GEG
        """

        filtered_list = [
            gwp_PE_Factor.relation_calorific_to_heating_value_GEG
            for gwp_PE_Factor in self.gwp_PE_Factors
            if gwp_PE_Factor.energy_carrier == fuel_type
        ]
        return filtered_list[0] if filtered_list else None

    def get_ghg_pe_conversion_factors(self, fuel_type):
        return (
            self.get_ghg_factor_heating(fuel_type),
            self.get_pe_factor_heating(fuel_type),
            self.get_conversion_factor_heating(fuel_type),
            fuel_type,
        )

    def check_heating_sys_electricity_sum(
            self,
            calculation_of_sum: CalculationOfSum,
            f_hs_hi: float,
            f_ghg: int,
            f_pe: float,
    ) -> Tuple[int, float, float, float]:
        """

        Args:
            calculation_of_sum: sum object
            f_hs_hi:
            f_ghg:
            f_pe:

        Returns:
            heating_sys_electricity_hi_sum, heating_sys_carbon_sum, heating_sys_pe_sum, heating_sys_fossils_hi_sum
        Return type
            Tuple[int, float, float, float]

        """
        heating_sys_electricity_hi_sum = 0
        heating_sys_fossils_hi_sum = 0

        if calculation_of_sum.Heating_Sys_Electricity_sum > 0:
            heating_sys_electricity_hi_sum = (
                    calculation_of_sum.Heating_Sys_Electricity_sum / f_hs_hi
            )
            heating_sys_carbon_sum = (heating_sys_electricity_hi_sum * f_ghg) / 1000
            heating_sys_pe_sum = heating_sys_electricity_hi_sum * f_pe
        else:
            heating_sys_fossils_hi_sum = (
                    calculation_of_sum.Heating_Sys_Fossils_sum / f_hs_hi
            )
            heating_sys_carbon_sum = (heating_sys_fossils_hi_sum * f_ghg) / 1000
            heating_sys_pe_sum = heating_sys_fossils_hi_sum * f_pe

        return (
            heating_sys_electricity_hi_sum,
            heating_sys_carbon_sum,
            heating_sys_pe_sum,
            heating_sys_fossils_hi_sum,
        )

    def check_hotwater_sys_electricity_sum(
            self,
            calculation_of_sum: CalculationOfSum,
            f_hs_hi: float,
            f_ghg: int,
            f_pe: float,
    ) -> Tuple[int, float, float, float]:
        """

        Args:
            calculation_of_sum: sum object
            f_hs_hi:
            f_ghg:
            f_pe:

        Returns:
            hot_water_sys_electricity_hi_sum, hot_water_sys_pe_sum, hot_water_sys_carbon_sum, hot_water_sys_fossils_hi_sum
        Return type
            Tuple[int, float, float, float]

        """
        hot_water_sys_electricity_hi_sum = 0
        hot_water_sys_fossils_hi_sum = 0

        if calculation_of_sum.HotWater_Sys_Electricity_sum > 0:
            hot_water_sys_electricity_hi_sum = (
                    calculation_of_sum.HotWater_Sys_Electricity_sum / f_hs_hi
            )
            hot_water_sys_pe_sum = hot_water_sys_electricity_hi_sum * f_pe
            hot_water_sys_carbon_sum = (hot_water_sys_electricity_hi_sum * f_ghg) / 1000
        else:
            hot_water_sys_fossils_hi_sum = (
                    calculation_of_sum.HotWater_Sys_Fossils_sum / f_hs_hi
            )
            hot_water_sys_pe_sum = hot_water_sys_fossils_hi_sum * f_pe
            hot_water_sys_carbon_sum = (hot_water_sys_fossils_hi_sum * f_ghg) / 1000
        return (
            hot_water_sys_electricity_hi_sum,
            hot_water_sys_pe_sum,
            hot_water_sys_carbon_sum,
            hot_water_sys_fossils_hi_sum,
        )

    def check_cooling_system_elctricity_sum(
            self,
            calculation_of_sum: CalculationOfSum,
            f_hs_hi: float,
            f_ghg: int,
            f_pe: float,
    ) -> Tuple[int, float, float, float]:
        """
        Args:
            calculation_of_sum: sum object
            f_hs_hi:
            f_ghg:
            f_pe:

        Returns:
            cooling_sys_electricity_hi_sum, cooling_sys_carbon_sum, cooling_sys_pe_sum, cooling_sys_fossils_hi_sum
        Return type
            Tuple[int, float, float, float]

        """
        cooling_sys_electricity_hi_sum = 0
        cooling_sys_fossils_hi_sum = 0

        if calculation_of_sum.Cooling_Sys_Electricity_sum > 0:
            cooling_sys_electricity_hi_sum = (
                    calculation_of_sum.Cooling_Sys_Electricity_sum / f_hs_hi
            )
            cooling_sys_carbon_sum = (cooling_sys_electricity_hi_sum * f_ghg) / 1000
            cooling_sys_pe_sum = cooling_sys_electricity_hi_sum * f_pe
        else:
            cooling_sys_fossils_hi_sum = (
                    calculation_of_sum.Cooling_Sys_Fossils_sum / f_hs_hi
            )
            cooling_sys_carbon_sum = (cooling_sys_fossils_hi_sum * f_ghg) / 1000
            cooling_sys_pe_sum = cooling_sys_fossils_hi_sum * f_pe
        return (
            cooling_sys_electricity_hi_sum,
            cooling_sys_carbon_sum,
            cooling_sys_pe_sum,
            cooling_sys_fossils_hi_sum,
        )

    def sys_electricity_folssils_sum(
            self, heating_sys_electricity_hi_sum: int, heating_sys_fossils_hi_sum: float
    ) -> float:
        """
        Calculates sum of heating_sys_electricity_hi_sum and heating_sys_fossils_hi_sum
        Args:
            heating_sys_electricity_hi_sum:
            heating_sys_fossils_hi_sum:

        Returns:
            heating_sys_electricity_hi_sum + heating_sys_fossils_hi_sum
        Return type
            float

        """
        return heating_sys_electricity_hi_sum + heating_sys_fossils_hi_sum

    def hot_energy_hi_sum(
            self, hotWater_sys_electricity_hi_sum: int, hot_water_sys_fossils_hi_sum: float
    ) -> float:
        """
        Calculates sum of hotWater_sys_electricity_hi_sum and hot_water_sys_fossils_hi_sum
        Args:
            hotWater_sys_electricity_hi_sum:
            hot_water_sys_fossils_hi_sum:

        Returns:
            hotWater_sys_electricity_hi_sum + hot_water_sys_fossils_hi_sum
        Return type
            float
        """
        return hotWater_sys_electricity_hi_sum + hot_water_sys_fossils_hi_sum

    def cooling_sys_hi_sum(
            self, cooling_sys_electricity_hi_sum: int, cooling_sys_fossils_hi_sum: float
    ) -> float:
        """
        Calculates sum of cooling_sys_electricity_hi_sum and cooling_sys_fossils_hi_sum
        Args:
            cooling_sys_electricity_hi_sum:
            cooling_sys_fossils_hi_sum:

        Returns:
            cooling_sys_electricity_hi_sum + cooling_sys_fossils_hi_sum
        Return type
            float

        """
        return cooling_sys_electricity_hi_sum + cooling_sys_fossils_hi_sum

    def check_if_central_dhw_use_same_fuel_type_as_heating_system(
            self, fuel_type
    ) -> str:
        """
        Checks if central dhw uses the same fuel type as the heating system
        Assumption: Central DHW-Systems use the same Fuel_type as Heating-Systems, only decentral DHW-Systems might have another Fuel-Type
        Args:
            fuel_type: fuel type

        Returns:
            fuel_type
        Return type
            str

        """

        if self.building_object.dhw_system == "DecentralElectricDHW":
            return "Electricity grid mix"
        elif self.building_object.dhw_system == "DecentralFuelBasedDHW":
            return "Natural gas"
        else:
            return fuel_type

    def air_cool(self) -> bool:
        """
        Checks if cooling supply system of the building in the list named air_cool
        Returns:
            True or False
        Return typ
            boolean

        """
        air_cool = [
            "AirCooledPistonScroll",
            "AirCooledPistonScrollMulti",
            "WaterCooledPistonScroll",
            "DirectCooler",
        ]
        return self.building_object.cooling_supply_system in air_cool

    def absorption_refrigeration_system(self) -> bool:
        """
         Checks if cooling supply system of the building is AbsorptionRefrigerationSystem
        Returns:
            True or False
        Return typ
            boolean

        """
        return (
                self.building_object.cooling_supply_system
                == "AbsorptionRefrigerationSystem"
        )

    def district_cooling(self) -> bool:
        """
        Checks if cooling supply system of the building is DistrictCooling
        Returns:
            True or False
        Return typ
            boolean

        """
        return self.building_object.cooling_supply_system == "DistrictCooling"

    def gas_engine_piston_scroll(self) -> bool:
        """
        Checks if cooling supply system of the building is GasEnginePistonScroll
        Returns:
            True or False
        Return typ
            boolean

        """
        return self.building_object.cooling_supply_system == "GasEnginePistonScroll"

    def no_cooling(self) -> bool:
        """
        Checks if cooling supply system of the building is NoCooling
        Returns:
            True or False
        Return typ
            boolean

        """
        return self.building_object.cooling_supply_system == "NoCooling"

    def choose_cooling_energy_fuel_type(self) -> Union[str, GHGEmissionError]:
        """

        Returns:
            fuel_type or throws an error
        Return type
            Union[str, GHGEmissionError]
        """
        try:
            if self.air_cool():
                return "Electricity grid mix"
            elif self.absorption_refrigeration_system():
                return "Waste Heat generated close to building"
            elif self.district_cooling():
                return "District cooling"
            elif self.gas_engine_piston_scroll():
                return "Natural gas"
            elif self.no_cooling():
                return "None"
            else:
                raise GHGEmissionError(
                    f"Error occured during calculation of GHG-Emission for Cooling. The following cooling_supply_system cannot be considered yet, {self.building_object.cooling_supply_system}"
                )
        except GHGEmissionError as error:
            print(error)
