from iso_simulator.model.calculations_sum import CalculationOfSum
from iso_simulator.model.location import Location
from iso_simulator.model.schedule_name import ScheduleName
from iso_simulator.model.weather_data import WeatherData
from iso_simulator.model.results import Result
from iso_simulator.model.window import Window
from iso_simulator.data_source.datasource_csv import DataSourceCSV
from iso_simulator.exceptions.ghg_emission import GHGEmissionError
from iso_simulator.exceptions.building_not_heated_exception import BuildingNotHeatedError

from typing import List, Tuple, Union
import time
import logging

logging.basicConfig(level=logging.INFO, filemode='w',
                    filename='calculations.log')

__author__ = "Wail Samjouni"
__copyright__ = "Copyright 2023, Institut Wohnen und Umwelt"
__license__ = "MIT"


class BuildingSimulator:

    def __init__(self,
                 datasourcecsv: DataSourceCSV,
                 weather_period: str,
                 profile_from_norm: str,
                 gains_from_group_values: str,
                 usage_from_norm: str
                 ):
        self.datasourcecsv = datasourcecsv
        self.weather_period = weather_period
        self.all_buildings = datasourcecsv.get_all_buildings()
        self.building_object = self.all_buildings[0]
        self.gwp_PE_Factors = datasourcecsv.get_epw_pe_factors()
        self.epw_object = datasourcecsv.get_epw_file(
            self.building_object.plz, self.weather_period)
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
        check_energy_ref_area = self.building_object.energy_ref_area == -8
        check_heating_supply_system = self.building_object.heating_supply_system == 'NoHeating'
        try:
            if check_energy_ref_area or check_heating_supply_system:
                raise BuildingNotHeatedError(f'Building {str(self.building_object.scr_gebaeude_id)} not heated')
        except BuildingNotHeatedError as error:
            print(error)

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
            self.building_object.hk_geb, self.building_object.uk_geb, self.usage_from_norm)
        return usage_start, usage_end

    def get_schedule(self) -> Union[Tuple[List[ScheduleName], str], ValueError]:
        return self.datasourcecsv.get_schedule(
            self.building_object.hk_geb, self.building_object.uk_geb)

    def get_tek(self) -> Union[Tuple[float, str], ValueError]:
        return self.datasourcecsv.get_tek(self.building_object.hk_geb, self.building_object.uk_geb)

    def get_occupancy_full_usage_hours(self) -> float:
        return self.datasourcecsv.get_schedule_sum(self.building_object.hk_geb, self.building_object.uk_geb)

    def get_weather_data(self) -> List[WeatherData]:
        return self.datasourcecsv.choose_and_get_the_right_weather_data_from_path(self.weather_period,
                                                                                  self.epw_object.file_name)

    def extract_outdoor_temperature(self, hour: int) -> float:
        """
        Extract the outdoor temperature in building_location for that hour from weather_data
        """
        return self.weather_data[hour].drybulb_C

    def extract_year(self, hour: int) -> int:
        return self.weather_data[hour].year

    def calc_altitude_and_azimuth(self, hour: int) -> Tuple[float, float]:
        """
        Call calc_sun_position(). Depending on latitude, longitude, year and hour - Independent from epw weather_data
        """
        location = Location()
        return location.calc_sun_position(
            self.epw_object.coordinates_station[0], self.epw_object.coordinates_station[1],
            self.extract_year(hour),
            hour)

    def calc_building_h_ve_adj(self, hour: int, t_out: float, usage_start: int, usage_end: int) -> float:
        """
        Calculate H_ve_adj, See building_physics for details
        """
        return self.building_object.calc_h_ve_adj(hour, t_out, usage_start, usage_end)

    def set_t_air_based_on_hour(self, hour: int) -> float:
        """
        Define t_air for calc_solar_gains(). Starting condition (hour==0) necessary for first time step 
        """
        t_air = self.building_object.t_set_heating if hour == 0 else self.building_object.t_air
        return t_air

    def calc_solar_gains_for_all_windows(self, sun_altitude: float, sun_azimuth: float,
                                         t_air: float, hour: int) -> None:
        """
        Calculate solar gains through each window 
        """

        for element in self.all_windows:
            element.calc_solar_gains(
                sun_altitude, sun_azimuth, self.weather_data[hour].dirnorrad_Whm2,
                self.weather_data[hour].difhorrad_Whm2, t_air,
                hour)

    def calc_illuminance_for_all_windows(self, sun_altitude: float, sun_azimuth: float,
                                         hour: int) -> None:
        """
        Calculate solar illuminance through each window 
        """

        for element in self.all_windows:
            element.calc_illuminance(
                sun_altitude, sun_azimuth, self.weather_data[hour].dirnorillum_lux,
                self.weather_data[hour].difhorillum_lux)

    def calc_occupancy(self, occupancy_schedule: List[ScheduleName], hour: int) -> float:
        """
        Calc occupancy for the time step
        """
        return occupancy_schedule[hour].People * self.building_object.max_occupancy

    def calc_sum_illuminance_all_windows(self) -> float:
        return sum(element.transmitted_illuminance for element in self.all_windows)

    def solve_building_lightning(self, occupancy_percent: float) -> None:
        """
        Calculate the lighting of the building for the time step
        """
        self.building_object.solve_building_lighting(
            self.calc_sum_illuminance_all_windows(), occupancy_percent)

    def calc_gains_from_occupancy_and_appliances(self, occupancy_schedule: List[ScheduleName], occupancy: float,
                                                 gain_per_person: float, appliance_gains: float, hour: int) -> float:
        """
        Calculate gains from occupancy and appliances
        This is thermal gains. Negative appliance_gains are heat sinks!
        """
        return occupancy * gain_per_person + appliance_gains * occupancy_schedule[
            hour].Appliances * self.building_object.energy_ref_area + self.building_object.lighting_demand

    def calc_appliance_gains_demand(self, occupancy_schedule: List[ScheduleName], appliance_gains: float,
                                    hour: int) -> float:
        """
        Calculate appliance_gains as part of the internal_gains
        """
        return appliance_gains * occupancy_schedule[hour].Appliances * self.building_object.energy_ref_area

    def get_appliance_gains_elt_demand(self, occupancy_schedule: List[ScheduleName], appliance_gains: float,
                                       hour: int) -> float:
        """
        Appliance_gains equal the electric energy that appliances use, except for negative appliance_gains of refrigerated counters in trade buildings for food!
        The assumption is: negative appliance_gains come from referigerated counters with heat pumps for which we assume a COP = 2.
        """
        appliance_gains_elt = -1 * appliance_gains / 2 if appliance_gains < 0 else appliance_gains
        return appliance_gains_elt * occupancy_schedule[hour].Appliances * self.building_object.energy_ref_area

    def calc_sum_solar_gains_all_windows(self) -> float:
        return sum(element.solar_gains for element in self.all_windows)

    def calc_energy_demand_for_time_step(self, internal_gains: float, t_out: float, t_m_prev: float) -> None:
        """
        Calculate energy demand for the time step 
        """
        self.building_object.solve_building_energy(
            internal_gains, self.calc_sum_solar_gains_all_windows(), t_out, t_m_prev)

    def check_if_central_heating_or_central_dhw(self) -> bool:
        central = ['CentralHeating', 'CentralDHW']
        return self.building_object.dhw_system in central

    def check_if_heat_pump_air_or_ground_source(self) -> bool:
        heat_source = ['HeatPumpAirSource', 'HeatPumpGroundSource', 'ElectricHeating']
        return self.building_object.heating_supply_system in heat_source

    def calc_hot_water_usage(self, occupancy_schedule: List[ScheduleName], tek_dhw_per_occupancy_full_usage_hour: float,
                             hour: int) -> Tuple[float, float, float, float]:
        """
        Calculate hot water usage of the building for the time step with (BuildingInstance.heating_energy / BuildingInstance.heating_demand)
        represents the Efficiency of the heat generation in the building
        :hotwaterdemand: in W
        """
        if self.building_object.dhw_system not in ['NoDHW', ' -']:
            hot_water_demand = occupancy_schedule[
                                   hour].People * tek_dhw_per_occupancy_full_usage_hour * 1000 * self.building_object.energy_ref_area

            if self.building_object.heating_demand > 0:
                hot_water_energy = hot_water_demand * (
                        self.building_object.heating_energy / self.building_object.heating_demand)
            else:
                hot_water_energy = hot_water_demand

            if self.building_object.dhw_system == 'DecentralElectricDHW' or (
                    self.check_if_central_heating_or_central_dhw() and self.check_if_heat_pump_air_or_ground_source()):
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

        return hot_water_demand, hot_water_energy, hot_water_sys_electricity, hot_water_sys_fossils

    # ----------------------------Extracted methods from choose the fuel type------------------------------------

    def biogas_boiler_types(self) -> bool:

        biogas_boiler_types = [
            'BiogasBoilerCondensingBefore95', 'BiogasBoilerCondensingFrom95']
        return self.building_object.heating_supply_system in biogas_boiler_types

    def biogas_oil_boilers_types(self) -> bool:
        biogas_oil_boilers_types = ['BiogasOilBoilerLowTempBefore95',
                                    'BiogasOilBoilerCondensingFrom95', 'BiogasOilBoilerCondensingImproved']
        return self.building_object.heating_supply_system in biogas_oil_boilers_types

    def oil_boiler_types(self) -> bool:
        oil_boiler_types = ['OilBoilerStandardBefore86', 'OilBoilerStandardFrom95', 'OilBoilerLowTempBefore87',
                            'OilBoilerLowTempBefore95',
                            'OilBoilerLowTempFrom95', 'OilBoilerCondensingBefore95', 'OilBoilerCondensingFrom95',
                            'OilBoilerCondensingImproved']
        return self.building_object.heating_supply_system in oil_boiler_types

    def lgas_boiler_temp(self) -> bool:
        lgas_boiler_temp = ['LGasBoilerLowTempBefore95', 'LGasBoilerLowTempFrom95', 'LGasBoilerCondensingBefore95',
                            'LGasBoilerCondensingFrom95', 'LGasBoilerCondensingImproved', 'LGasBoilerLowTempBefore87']
        return self.building_object.heating_supply_system in lgas_boiler_temp

    def gas_boiler_standard(self) -> bool:
        gas_boiler_standard = ['GasBoilerStandardBefore86', 'GasBoilerStandardBefore95', 'GasBoilerStandardFrom95',
                               'GasBoilerLowTempBefore87', 'GasBoilerLowTempBefore95',
                               'GasBoilerLowTempFrom95', 'GasBoilerLowTempSpecialFrom78',
                               'GasBoilerLowTempSpecialFrom95', 'GasBoilerCondensingBefore95',
                               'GasBoilerCondensingImproved', 'GasBoilerCondensingFrom95']
        return self.building_object.heating_supply_system in gas_boiler_standard

    def coal_solid_fuel_boiler(self) -> bool:
        return self.building_object.heating_supply_system == 'CoalSolidFuelBoiler'

    def solid_fuel_liquid_fuel_furnace(self) -> bool:
        return self.building_object.heating_supply_system == 'SolidFuelLiquidFuelFurnace'

    def heat_pump(self) -> bool:
        heat_pumping = ['HeatPumpAirSource', 'HeatPumpGroundSource']
        return self.building_object.heating_supply_system in heat_pumping

    def wood(self) -> bool:
        wood = ['WoodChipSolidFuelBoiler',
                'WoodPelletSolidFuelBoiler', 'WoodSolidFuelBoilerCentral']
        return self.building_object.heating_supply_system in wood

    def gas_chip(self) -> bool:
        return self.building_object.heating_supply_system == 'GasCHP'

    def district_heating(self) -> bool:
        return self.building_object.heating_supply_system == 'DistrictHeating'

    def electric_heating(self) -> bool:
        return self.building_object.heating_supply_system == 'ElectricHeating'

    def direct_heater(self) -> bool:
        return self.building_object.heating_supply_system == 'DirectHeater'

    def no_heating(self) -> bool:
        return self.building_object.heating_supply_system == 'NoHeating'

    def lgas_gas_gas_chip(self) -> bool:
        return self.lgas_boiler_temp() | self.gas_boiler_standard() | self.gas_chip()

    def heat_pump_or_electric_heating(self) -> bool:
        return self.heat_pump() | self.electric_heating()

    def hard_coal(self) -> bool:
        return self.coal_solid_fuel_boiler() or self.solid_fuel_liquid_fuel_furnace()

    def choose_the_fuel_type(self) -> Union[str, GHGEmissionError]:

        try:
            if self.biogas_boiler_types():
                return 'Biogas (general)'

            elif self.biogas_oil_boilers_types():
                return 'Biogas Bio-oil Mix (general)'

            elif self.oil_boiler_types():
                return 'Light fuel oil'
            elif self.lgas_gas_gas_chip():
                return 'Natural gas'
            elif self.wood():
                return 'Wood'
            elif self.hard_coal():
                return 'Hard coal'
            elif self.heat_pump_or_electric_heating:
                return 'Electricity grid mix'
            elif self.district_heating():
                return 'District heating (Combined Heat and Power) Gas or Liquid fuels'
            elif self.direct_heater():
                return 'District heating (Combined Heat and Power) Coal'
            elif self.no_heating():
                return 'None'
            else:
                raise GHGEmissionError(
                    "Error occured during calculation of GHG-Emission for Heating. The following heating_supply_system cannot be considered yet")
        except GHGEmissionError as error:
            print(error)

    # ----------------------------------------------End Choose Fuel Type---------------------------------------------------------------

    def get_ghg_factor_heating(self, fuel_type: str):
        """
        GHG-Faktor Heating
        """

        filtered_list = [
            gwp_PE_Factor.gwp_spezific_to_heating_value_GEG for gwp_PE_Factor in self.gwp_PE_Factors if
            gwp_PE_Factor.energy_carrier == fuel_type]
        return filtered_list[0] if filtered_list else None

    def get_pe_factor_heating(self, fuel_type: str):
        """
        PE-Faktor Heating
        """

        filtered_list = [
            gwp_PE_Factor.primary_energy_factor_GEG for gwp_PE_Factor in self.gwp_PE_Factors if
            gwp_PE_Factor.energy_carrier == fuel_type]
        return filtered_list[0] if filtered_list else None

    def get_conversion_factor_heating(self, fuel_type: str):
        """
        Umrechnungsfaktor von Brennwert (Hs) zu Heizwert (Hi) einlesen
        """

        filtered_list = [
            gwp_PE_Factor.relation_calorific_to_heating_value_GEG for gwp_PE_Factor in self.gwp_PE_Factors if
            gwp_PE_Factor.energy_carrier == fuel_type]
        return filtered_list[0] if filtered_list else None

    def get_ghg_pe_conversion_factors(self, fuel_type):
        return self.get_ghg_factor_heating(fuel_type), self.get_pe_factor_heating(
            fuel_type), self.get_conversion_factor_heating(fuel_type), fuel_type

    def check_heating_sys_electricity_sum(self, calculation_of_sum: CalculationOfSum, f_hs_hi: float, f_ghg: int,
                                          f_pe: float) -> Tuple[int, float, float, float]:
        """
        :Heating_Sys_Electricity_Hi_sum: for kWhHi Final Energy Demand
        :Heating_Sys_Carbon_sum: for kg CO2eq
        :Heating_Sys_PE_sum: for kWh Primary Energy Demand
        :Heating_Sys_Fossils_Hi_sum: for kWhHi Final Energy Demand
        :Heating_Sys_Carbon_sum: for kg CO2eq
        :Heating_Sys_PE_sum: for kWh Primary Energy Demand
        """
        heating_sys_electricity_hi_sum = 0
        heating_sys_fossils_hi_sum = 0

        if calculation_of_sum.Heating_Sys_Electricity_sum > 0:
            heating_sys_electricity_hi_sum = calculation_of_sum.Heating_Sys_Electricity_sum / f_hs_hi
            heating_sys_carbon_sum = (
                                             heating_sys_electricity_hi_sum * f_ghg) / 1000
            heating_sys_pe_sum = heating_sys_electricity_hi_sum * f_pe
        else:
            heating_sys_fossils_hi_sum = calculation_of_sum.Heating_Sys_Fossils_sum / f_hs_hi
            heating_sys_carbon_sum = (
                                             heating_sys_fossils_hi_sum * f_ghg) / 1000
            heating_sys_pe_sum = heating_sys_fossils_hi_sum * f_pe

        return heating_sys_electricity_hi_sum, heating_sys_carbon_sum, heating_sys_pe_sum, heating_sys_fossils_hi_sum

    def check_hotwater_sys_electricity_sum(self, calculation_of_sum: CalculationOfSum, f_hs_hi: float, f_ghg: int,
                                           f_pe: float) -> Tuple[int, float, float, float]:

        hot_water_sys_electricity_hi_sum = 0
        hot_water_sys_fossils_hi_sum = 0

        if calculation_of_sum.HotWater_Sys_Electricity_sum > 0:
            hot_water_sys_electricity_hi_sum = calculation_of_sum.HotWater_Sys_Electricity_sum / f_hs_hi
            hot_water_sys_pe_sum = hot_water_sys_electricity_hi_sum * f_pe
            hot_water_sys_carbon_sum = (
                                               hot_water_sys_electricity_hi_sum * f_ghg) / 1000
        else:
            hot_water_sys_fossils_hi_sum = calculation_of_sum.HotWater_Sys_Fossils_sum / f_hs_hi
            hot_water_sys_pe_sum = hot_water_sys_fossils_hi_sum * f_pe
            hot_water_sys_carbon_sum = (
                                               hot_water_sys_fossils_hi_sum * f_ghg) / 1000
        return hot_water_sys_electricity_hi_sum, hot_water_sys_pe_sum, hot_water_sys_carbon_sum, hot_water_sys_fossils_hi_sum

    def check_cooling_system_elctricity_sum(self, calculation_of_sum: CalculationOfSum, f_hs_hi: float, f_ghg: int,
                                            f_pe: float) -> Tuple[int, float, float, float]:
        """
        :Cooling_Sys_Electricity_Hi_sum: for kWhHi Final Energy Demand
        :Cooling_Sys_Carbon_sum: for kg CO2eq
        :Cooling_Sys_PE_sum: for kWh Primary Energy Demand
        :Cooling_Sys_Fossils_Hi_sum: for kWhHi Final Energy Demand
        :Cooling_Sys_Carbon_sum: for kg CO2eq
        :Cooling_Sys_PE_sum: for kWh Primary Energy Demand
        """
        cooling_sys_electricity_hi_sum = 0
        cooling_sys_fossils_hi_sum = 0

        if calculation_of_sum.Cooling_Sys_Electricity_sum > 0:
            cooling_sys_electricity_hi_sum = calculation_of_sum.Cooling_Sys_Electricity_sum / f_hs_hi
            cooling_sys_carbon_sum = (
                                             cooling_sys_electricity_hi_sum * f_ghg) / 1000
            cooling_sys_pe_sum = cooling_sys_electricity_hi_sum * f_pe
        else:
            cooling_sys_fossils_hi_sum = calculation_of_sum.Cooling_Sys_Fossils_sum / f_hs_hi
            cooling_sys_carbon_sum = (cooling_sys_fossils_hi_sum * f_ghg) / 1000
            cooling_sys_pe_sum = cooling_sys_fossils_hi_sum * f_pe
        return cooling_sys_electricity_hi_sum, cooling_sys_carbon_sum, cooling_sys_pe_sum, cooling_sys_fossils_hi_sum

    # -----------------------------------Sum Electricity Fossil, Hot Energy and Cooling System--------------------------------------------------
    def sys_electricity_folssils_sum(self, heating_sys_electricity_hi_sum: int,
                                     heating_sys_fossils_hi_sum: float) -> float:
        return heating_sys_electricity_hi_sum + heating_sys_fossils_hi_sum

    def hot_energy_hi_sum(self, hotWater_sys_electricity_hi_sum: int,
                          hot_water_sys_fossils_hi_sum: float):
        return hotWater_sys_electricity_hi_sum + hot_water_sys_fossils_hi_sum

    def cooling_sys_hi_sum(self, cooling_sys_electricity_hi_sum: int, cooling_sys_fossils_hi_sum:
    float) -> float:
        return cooling_sys_electricity_hi_sum + cooling_sys_fossils_hi_sum

    # -----------------------------------End Sum Electricity Fossil, Hot Energy and Cooling System-----------------------------------------------

    def check_if_central_dhw_use_same_fuel_type_as_heating_system(self, fuel_type) -> str:
        """
        HOT WATER
        Assumption: Central DHW-Systems use the same Fuel_type as Heating-Systems, only decentral DHW-Systems might have another Fuel-Type
        """
        if self.building_object.dhw_system == 'DecentralElectricDHW':
            return 'Electricity grid mix'
        elif self.building_object.dhw_system == 'DecentralFuelBasedDHW':
            return 'Natural gas'
        else:
            return fuel_type

    # ------------------------------------------------------------Cooling Energy----------------------------------------------------------------
    def air_cool(self) -> bool:
        air_cool = ['AirCooledPistonScroll', 'AirCooledPistonScrollMulti',
                    'WaterCooledPistonScroll', 'DirectCooler']
        return self.building_object.cooling_supply_system in air_cool

    def absorption_refrigeration_system(self) -> bool:
        return self.building_object.cooling_supply_system == 'AbsorptionRefrigerationSystem'

    def district_cooling(self) -> bool:
        return self.building_object.cooling_supply_system == 'DistrictCooling'

    def gas_engine_piston_scroll(self):
        return self.building_object.cooling_supply_system == 'GasEnginePistonScroll'

    def no_cooling(self) -> bool:
        return self.building_object.cooling_supply_system == 'NoCooling'

    def choose_cooling_energy_fuel_type(self) -> Union[str, GHGEmissionError]:
        try:
            if self.air_cool():
                return 'Electricity grid mix'
            elif self.absorption_refrigeration_system():
                return 'Waste Heat generated close to building'
            elif self.district_cooling():
                return 'District cooling'
            elif self.gas_engine_piston_scroll():
                return 'Natural gas'
            elif self.no_cooling():
                return 'None'
            else:
                raise GHGEmissionError(
                    f"Error occured during calculation of GHG-Emission for Cooling. The following cooling_supply_system cannot be considered yet, {self.building_object.cooling_supply_system}")
        except GHGEmissionError as error:
            print(error)
