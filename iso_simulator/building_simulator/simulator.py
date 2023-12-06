from iso_simulator.model.calculations_sum import CalculationOfSum
from iso_simulator.model.location import Location
from iso_simulator.model.schedule_name import ScheduleName
from iso_simulator.model.weather_data import WeatherData
from iso_simulator.model.results import Result
from iso_simulator.model.window import Window
from iso_simulator.data_source.datasource_csv import DataSourceCSV
from iso_simulator.exceptions.ghg_emission import GHGEmissionException

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

    def get_occupancy_full_usage_hours(self) -> float:
        return self.datasourcecsv.get_schedule_sum(self.building_object.hk_geb, self.building_object.uk_geb)

    def get_weather_data(self) -> List[WeatherData]:
        epw_object = self.datasourcecsv.get_epw_file(
            self.building_object.plz, self.weather_period)
        return self.datasourcecsv.choose_and_get_the_right_weather_data_from_path(self.weather_period,
                                                                                  epw_object.file_name)

    def extract_outdoor_temperature(self, weather_data: List[WeatherData], hour: int) -> float:
        """
        Extract the outdoor temperature in building_location for that hour from weather_data
        """
        return weather_data[hour].drybulb_C

    def extract_year(self, weather_data: List[WeatherData], hour: int) -> int:
        return weather_data[hour].year

    def calc_altitude_and_zimuth(self, hour: int) -> Tuple[float, float]:
        """
        Call calc_sun_position(). Depending on latitude, longitude, year and hour - Independent from epw weather_data
        """
        location = Location()
        epw_file = self.datasourcecsv.get_epw_file(
            self.building_object.plz, self.weather_period)
        weather_data = self.datasourcecsv.choose_and_get_the_right_weather_data_from_path(
            self.weather_period, epw_file.file_name)
        return location.calc_sun_position(
            epw_file.coordinates_station[0], epw_file.coordinates_station[1], self.extract_year(weather_data, hour),
            hour)

    def calc_building_h_ve_adj(self, hour: int, t_out: float, usage_start: int, usage_end: int) -> float:
        """
        Calculate H_ve_adj, See building_physics for details
        """
        return self.building_object.calc_h_ve_adj(hour, t_out, usage_start, usage_end)

    def set_t_air_based_on_hour(self, hour) -> float:
        """
        Define t_air for calc_solar_gains(). Starting condition (hour==0) necessary for first time step 
        """
        t_air = self.building_object.t_set_heating if hour == 0 else self.building_object.t_air
        return t_air

    def calc_solar_gains_for_all_windows(self, weather_data: List[WeatherData], sun_altitude: float, sun_azimuth: float,
                                         t_air: float, hour: int) -> None:
        """
        Calculate solar gains through each window 
        """

        for element in self.all_windows:
            element.calc_solar_gains(
                sun_altitude, sun_azimuth, weather_data[hour].dirnorrad_Whm2, weather_data[hour].difhorrad_Whm2, t_air,
                hour)

    def calc_illuminance_for_all_windows(self, weather_data: List[WeatherData], sun_altitude: float, sun_azimuth: float,
                                         hour: int) -> None:
        """
        Calculate solar illuminance through each window 
        """

        for element in self.all_windows:
            element.calc_illuminance(
                sun_altitude, sun_azimuth, weather_data[hour].dirnorillum_lux, weather_data[hour].difhorillum_lux)

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
        appliance_gains_elt = -1 * appliance_gains / \
                              2 if appliance_gains < 0 else appliance_gains
        return appliance_gains_elt * occupancy_schedule[hour].Appliances * self.building_object.energy_ref_area

    def calc_sum_solar_gains_all_windows(self) -> float:
        return sum(element.solar_gains for element in self.all_windows)

    def calc_energy_demand_for_time_step(self, internal_gains: float, t_out: float, t_m_prev: int) -> None:
        """
        Calculate energy demand for the time step 
        """
        self.building_object.solve_building_energy(
            internal_gains, self.calc_sum_solar_gains_all_windows(), t_out, t_m_prev)

    def check_if_central_heating_or_central_dhw(self) -> bool:
        central = ['CentralHeating', 'CentralDHW']
        return self.building_object.dhw_system in central

    def check_if_heat_pump_air_source_or_heat_pump_ground_source(self):
        heat_source = ['HeatPumpAirSource', 'HeatPumpGroundSource']
        return self.building_object.heating_supply_system in heat_source

    def calc_hot_water_usage(self, occupancy_schedule: List[ScheduleName], tek_dhw_per_occupancy_full_usage_hour: float,
                             hour: int):
        """
        Calculate hot water usage of the building for the time step with (BuildingInstance.heating_energy / BuildingInstance.heating_demand)
        represents the Efficiency of the heat generation in the building
        :hotwaterdemand: in W
        """

        if self.building_object.dhw_system not in ['NoDHW', ' -']:
            hot_water_demand = occupancy_schedule[hour].People * \
                             tek_dhw_per_occupancy_full_usage_hour * \
                             1000 * self.building_object.energy_ref_area

            if self.building_object.heating_demand > 0:  # catch devision by zero error
                hot_water_energy = hot_water_demand * \
                                 (self.building_object.heating_energy /
                                  self.building_object.heating_demand)
            else:
                hot_water_energy = hot_water_demand

            if self.building_object.dhw_system == 'DecentralElectricDHW' or (
                    self.check_if_central_heating_or_central_dhw() and (
                    self.check_if_heat_pump_air_source_or_heat_pump_ground_source() | self.building_object.heating_supply_system == 'ElectricHeating')):
                self.result.HotWaterSysElectricity = hot_water_energy
                self.result.HotWaterSysFossils = 0
            else:
                self.result.HotWaterSysFossils = hot_water_energy
                self.resultHotWaterSysElectricity = 0
        else:
            self.result.hot_water_demand = 0
            self.result.hot_water_energy = 0
            self.result.HotWaterSysElectricity = 0
            self.result.HotWaterSysFossils = 0

        return self.result

    # -------------------------------------Extracted methods from append_results() --------------------------------------------------
    def heating_demand_and_energy_result(self) -> None:
        self.result.HeatingDemand.append(self.building_object.heating_demand)
        self.result.HeatingEnergy.append(self.building_object.heating_energy)

    def heating_electricity_fossils_sys_results(self) -> None:
        self.result.Heating_Sys_Electricity.append(
            self.building_object.heating_sys_electricity)
        self.result.Heating_Sys_Fossils.append(
            self.building_object.heating_sys_fossils)

    def cooling_electricity_fossils_sys_results(self) -> None:
        self.result.Cooling_Sys_Electricity.append(
            self.building_object.cooling_sys_electricity)
        self.result.Cooling_Sys_Fossils.append(
            self.building_object.cooling_sys_fossils)

    def cooling_demand_and_energy_result(self) -> None:
        self.result.CoolingDemand.append(self.building_object.cooling_demand)
        self.result.CoolingEnergy.append(self.building_object.cooling_energy)

    def hot_demand_and_energy_result(self) -> None:
        self.result.HotWaterDemand.append(self.result.hotwaterdemand)
        self.result.HotWaterEnergy.append(self.result.hotwaterenergy)

    def hotwater_electricity_fossils_sys_results(self) -> None:
        self.result.HotWater_Sys_Electricity.append(
            self.result.HotWaterSysElectricity)
        self.result.HotWater_Sys_Fossils.append(self.result.HotWaterSysFossils)

    def air_temperature_results(self, t_out: float) -> None:
        self.result.TempAir.append(self.building_object.t_air)
        self.result.OutsideTemp.append(t_out)

    def south_east_windows_results(self) -> None:
        self.result.SolarGainsSouthWindow.append(
            self.all_windows[0].solar_gains)
        self.result.SolarGainsEastWindow.append(
            self.all_windows[1].solar_gains)

    def west_north_windows_results(self) -> None:
        self.result.SolarGainsWestWindow.append(
            self.all_windows[2].solar_gains)
        self.result.SolarGainsNorthWindow.append(
            self.all_windows[3].solar_gains)

    def all_windows_results(self) -> None:
        self.south_east_windows_results()
        self.west_north_windows_results()

    def solar_gains_daytime_results(self, hour: int) -> None:
        self.result.SolarGainsTotal.append(
            self.calc_sum_solar_gains_all_windows())
        self.result.DayTime.append(hour % 24)

    def append_results(self, internal_gains: float, t_out: float, hour: int) -> None:
        """
        Append results to the result object
        """

        self.result.scr_gebaeude_id = self.building_object.scr_gebaeude_id

        self.heating_demand_and_energy_result()
        self.heating_electricity_fossils_sys_results()
        self.cooling_demand_and_energy_result()
        self.cooling_electricity_fossils_sys_results()
        self.hot_demand_and_energy_result()
        self.hotwater_electricity_fossils_sys_results()
        self.air_temperature_results()

        self.result.LightingDemand.append(self.building_object.lighting_demand)
        self.result.InternalGains.append(internal_gains)

        self.all_windows_results()
        self.solar_gains_daytime_results(hour)

    # -----------------------------------------------------------------------------------------------------

    def calcs_for_console_prints(self, resuls: Result):
        """
        These are helpful calculations for the console prints
        """
        return CalculationOfSum(sum(resuls.HeatingDemand) / 1000, sum(resuls.HeatingEnergy) / 1000,
                                sum(resuls.Heating_Sys_Electricity) /
                                1000, sum(resuls.Heating_Sys_Fossils) / 1000,
                                sum(resuls.CoolingDemand) /
                                1000, sum(resuls.CoolingEnergy) / 1000,
                                sum(resuls.Cooling_Sys_Electricity) /
                                1000, sum(resuls.Cooling_Sys_Electricity) / 1000,
                                sum(resuls.Cooling_Sys_Fossils) /
                                1000, sum(resuls.HotWaterDemand) / 1000,
                                sum(resuls.HotWaterEnergy) /
                                1000, sum(
                resuls.HotWater_Sys_Electricity) / 1000,
                                sum(resuls.HotWater_Sys_Fossils) /
                                1000, sum(resuls.InternalGains) / 1000,
                                sum(resuls.Appliance_gains_demand) /
                                1000, sum(resuls.Appliance_gains_demand) / 1000,
                                sum(resuls.Appliance_gains_elt_demand) /
                                1000, sum(resuls.LightingDemand) / 1000,
                                sum(resuls.SolarGainsSouthWindow) /
                                1000, sum(resuls.SolarGainsEastWindow) / 1000,
                                sum(resuls.SolarGainsWestWindow) /
                                1000, sum(resuls.SolarGainsNorthWindow) / 1000,
                                sum(resuls.SolarGainsTotal) / 1000)

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
        self.building_object.heating_supply_system in lgas_boiler_temp

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
        return self.coal_solid_fuel_boiler() | self.solid_fuel_liquid_fuel_furnace()

    def choose_the_fuel_type(self) -> Union[str, None]:

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
        except GHGEmissionException as exception:
            print(exception.message)

            # print(
            #     "Error occured during calculation of GHG-Emission for Heating. The following heating_supply_system cannot be considered yet",
            #     self.building_object.heating_supply_system)

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

    def check_heating_sys_electricity_sum(self, calculation_of_sum: CalculationOfSum, f_Hs_Hi: float, f_GHG: int,
                                          f_PE: float) -> Tuple[int, float, float, float]:
        """
        :Heating_Sys_Electricity_Hi_sum: for kWhHi Final Energy Demand
        :Heating_Sys_Carbon_sum: for kg CO2eq
        :Heating_Sys_PE_sum: for kWh Primary Energy Demand
        :Heating_Sys_Fossils_Hi_sum: for kWhHi Final Energy Demand
        :Heating_Sys_Carbon_sum: for kg CO2eq
        :Heating_Sys_PE_sum: for kWh Primary Energy Demand
        """

        if calculation_of_sum.Heating_Sys_Electricity_sum > 0:
            Heating_Sys_Electricity_Hi_sum = calculation_of_sum.Heating_Sys_Electricity_sum / f_Hs_Hi
            Heating_Sys_Carbon_sum = (
                                             Heating_Sys_Electricity_Hi_sum * f_GHG) / 1000
            Heating_Sys_PE_sum = Heating_Sys_Electricity_Hi_sum * f_PE
        else:
            Heating_Sys_Fossils_Hi_sum = calculation_of_sum.Heating_Sys_Fossils_sum / f_Hs_Hi
            Heating_Sys_Carbon_sum = (
                                             Heating_Sys_Fossils_Hi_sum * f_GHG) / 1000
            Heating_Sys_PE_sum = Heating_Sys_Fossils_Hi_sum * f_PE

        return Heating_Sys_Electricity_Hi_sum, Heating_Sys_Carbon_sum, Heating_Sys_PE_sum, Heating_Sys_Fossils_Hi_sum

    def check_hotwater_sys_electricity_sum(self, calculation_of_sum: CalculationOfSum, f_Hs_Hi: float, f_GHG: int,
                                           f_PE: float) -> Tuple[int, float, float, float]:

        if calculation_of_sum.HotWater_Sys_Electricity_sum > 0:
            HotWater_Sys_Electricity_Hi_sum = calculation_of_sum.HotWater_Sys_Electricity_sum / f_Hs_Hi
            HotWater_Sys_PE_sum = HotWater_Sys_Electricity_Hi_sum * f_PE
            HotWater_Sys_Carbon_sum = (
                                              HotWater_Sys_Electricity_Hi_sum * f_GHG) / 1000
        else:
            HotWater_Sys_Fossils_Hi_sum = calculation_of_sum.HotWater_Sys_Fossils_sum / f_Hs_Hi
            HotWater_Sys_PE_sum = HotWater_Sys_Fossils_Hi_sum * f_PE
            HotWater_Sys_Carbon_sum = (
                                              HotWater_Sys_Fossils_Hi_sum * f_GHG) / 1000
        return HotWater_Sys_Electricity_Hi_sum, HotWater_Sys_PE_sum, HotWater_Sys_Carbon_sum, HotWater_Sys_Fossils_Hi_sum

    def check_cooling_system_elctricity_sum(self, calculation_of_sum: CalculationOfSum, f_Hs_Hi: float, f_GHG: int,
                                            f_PE: float) -> Tuple[int, float, float, float]:
        """
        :Cooling_Sys_Electricity_Hi_sum: for kWhHi Final Energy Demand
        :Cooling_Sys_Carbon_sum: for kg CO2eq
        :Cooling_Sys_PE_sum: for kWh Primary Energy Demand
        :Cooling_Sys_Fossils_Hi_sum: for kWhHi Final Energy Demand
        :Cooling_Sys_Carbon_sum: for kg CO2eq
        :Cooling_Sys_PE_sum: for kWh Primary Energy Demand
        """
        if calculation_of_sum.Cooling_Sys_Electricity_sum > 0:
            Cooling_Sys_Electricity_Hi_sum = calculation_of_sum.Cooling_Sys_Electricity_sum / f_Hs_Hi
            Cooling_Sys_Carbon_sum = (
                                             Cooling_Sys_Electricity_Hi_sum * f_GHG) / 1000
            Cooling_Sys_PE_sum = Cooling_Sys_Electricity_Hi_sum * f_PE
        else:
            Cooling_Sys_Fossils_Hi_sum = calculation_of_sum.Cooling_Sys_Fossils_sum / f_Hs_Hi
            Cooling_Sys_Carbon_sum = (
                                             Cooling_Sys_Fossils_Hi_sum * f_GHG) / 1000
            Cooling_Sys_PE_sum = Cooling_Sys_Fossils_Hi_sum * f_PE
        return Cooling_Sys_Electricity_Hi_sum, Cooling_Sys_Carbon_sum, Cooling_Sys_PE_sum, Cooling_Sys_Fossils_Hi_sum

    # -----------------------------------Sum Electricity Fossil, Hot Energy and Cooling System--------------------------------------------------
    def sys_electricity_folssils_sum(self, heating_sys_electricity_hi_sum: int,
                                     heating_sys_fossils_hi_sum: float) -> float:
        return heating_sys_electricity_hi_sum + heating_sys_fossils_hi_sum

    def hot_energy_hi_sum(self, hotWater_sys_electricity_hi_sum: int,
                          hotWater_sys_fossils_hi_sum: float):
        return hotWater_sys_electricity_hi_sum + hotWater_sys_fossils_hi_sum

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

    def choose_cooling_energy_fuel_type(self) -> Union[str, None]:

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
            print(
                "Error occured during calculation of GHG-Emission for Cooling. The following cooling_supply_system cannot be considered yet",
                self.building_object.cooling_supply_system)
    # ---------------------------------------------------------End Cooling Energy-----------------------------------------------------------------
