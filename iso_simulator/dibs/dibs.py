from iso_simulator.data_source.datasource import DataSource
from iso_simulator.data_source.datasource_csv import DataSourceCSV
from iso_simulator.building_simulator.simulator import BuildingSimulator
from typing import Tuple, List
from iso_simulator.model.schedule_name import ScheduleName
from iso_simulator.model.results import Result
from iso_simulator.model.ResultOutput import ResultOutput


class DIBS:
    def __init__(self, datasource: DataSourceCSV):
        self.datasource = datasource

    def set_data_source(self, datasource: DataSource):
        self.datasource = datasource

    def calculate_building_result(self, weather_period: str, profile_from_norm: str, gains_from_group_values: str,
                                  usage_from_norm: str):
        simulator = BuildingSimulator(self.datasource, weather_period, profile_from_norm, gains_from_group_values,
                                      usage_from_norm)

        simulator.initialize_building_time()

        building_data = simulator.datasourcecsv.get_building_data()

        result = Result()

        simulator.check_energy_area_and_heating()

        epw_file_object = simulator.datasourcecsv.get_epw_file(simulator.building_object.plz, simulator.weather_period)

        gain_person_and_typ_norm, appliance_gains = simulator.datasourcecsv.get_gains(simulator.building_object.hk_geb,
                                                                                      simulator.building_object.uk_geb,
                                                                                      simulator.profile_from_norm,
                                                                                      simulator.gains_from_group_values)

        gain_per_person, typ_norm = gain_person_and_typ_norm

        usage_start, usage_end = simulator.get_usage_start_and_end()

        occupancy_schedule, schedule_name = simulator.get_schedule()

        tek_dhw, tek_name = simulator.get_tek()

        occupancy_full_usage_hours = simulator.get_occupancy_full_usage_hours()

        tek_dhw_per_occupancy_full_usage_hour = tek_dhw / occupancy_full_usage_hours

        t_m_prev = simulator.building_object.t_start

        for hour in range(8760):
            t_out = simulator.extract_outdoor_temperature(hour)

            altitude, azimuth = simulator.calc_altitude_and_azimuth(hour)

            simulator.building_object.h_ve_adj = simulator.building_object.calc_h_ve_adj(hour, t_out, usage_start,
                                                                                         usage_end)

            t_air = simulator.set_t_air_based_on_hour(hour)

            simulator.calc_solar_gains_for_all_windows(altitude, azimuth, t_air, hour)
            simulator.calc_illuminance_for_all_windows(altitude, azimuth, hour)

            occupancy_percent = occupancy_schedule[hour].People
            occupancy = simulator.calc_occupancy(occupancy_schedule, hour)

            simulator.building_object.solve_building_lighting(simulator.calc_sum_illuminance_all_windows(),
                                                              occupancy_percent)

            internal_gains = simulator.calc_gains_from_occupancy_and_appliances(occupancy_schedule, occupancy,
                                                                                gain_per_person, appliance_gains, hour)

            """
            Calculate appliance_gains as part of the internal_gains
            """
            appliance_gains_demand = simulator.calc_appliance_gains_demand(occupancy_schedule, appliance_gains, hour)
            """
            Appliance_gains equal the electric energy that appliances use, except for negative appliance_gains of refrigerated counters in trade buildings for food!
            The assumption is: negative appliance_gains come from referigerated counters with heat pumps for which we assume a COP = 2.
            """
            appliance_gains_demand_elt = simulator.get_appliance_gains_elt_demand(occupancy_schedule, appliance_gains,
                                                                                  hour)

            """
            Calculate energy demand for the time step
            """
            simulator.calc_energy_demand_for_time_step(internal_gains, t_out, t_m_prev)
            print(f'hour: {hour}, heating_demand: {simulator.building_object.heating_demand}')

            """
            Calculate hot water usage of the building for the time step with (BuildingInstance.heating_energy
             / BuildingInstance.heating_demand) represents the Efficiency of the heat generation in the building
            """

            hot_water_demand, hot_water_energy, hot_water_sys_electricity, hot_water_sys_fossils = simulator.calc_hot_water_usage(
                occupancy_schedule, tek_dhw_per_occupancy_full_usage_hour, hour)

            """
            Set the previous temperature for the next time step
            """
            t_m_prev = simulator.building_object.t_m_next
            print(t_m_prev)
            """
            Append results to the created lists 
            """
            result.append_results(simulator.building_object, simulator.all_windows, hot_water_demand, hot_water_energy,
                                  hot_water_sys_electricity, hot_water_sys_fossils, t_out, internal_gains,
                                  appliance_gains_demand, appliance_gains_demand_elt,
                                  simulator.calc_sum_solar_gains_all_windows(), hour)
        """
        Some calculations used for the console prints
        """

        sum_of_all_results = result.calc_sum_of_results()
        # print(f' heating_demand : {sum(result.heating_demand)}')
        # print(f' heating_energy : {sum(result.heating_energy)}')
        # print(f'heating_sys_electricity : {sum(result.heating_sys_electricity)}')
        # print(f'heating_sys_fossils : {sum(result.heating_sys_fossils)}')
        # print(f'heating_sys_fossils : {sum(result.cooling_demand)}')
        # print(f'heating_sys_fossils : {sum(result.cooling_energy)}')
        # print(f'heating_sys_fossils : {sum(result.cooling_sys_electricity)}')
        # print(f'heating_sys_fossils : {sum(result.cooling_sys_fossils)}')
        # print(f'heating_sys_fossils : {sum(result.all_hot_water_demand)}')
        # print(f'heating_sys_fossils : {sum(result.all_hot_water_energy)}')
        # print(f'heating_sys_fossils : {sum(result.hot_water_sys_electricity)}')
        # print(f'heating_sys_fossils : {sum(result.hot_water_sys_fossils)}')
        """
        the fuel-related final energy sums, f.i. HeatingEnergy_sum, are calculated based upon the superior heating value
        Hs since the corresponding expenditure factors from TEK 9.24 represent the ration of Hs-related final energy to 
        useful energy.
         --- Calculation  related to HEATING and Hotwater energy ---
        """
        fuel_type = simulator.choose_the_fuel_type()

        """
        Heating:
            - GHG-Factor Heating
            - PE-Factor Heating
            - Umrechnungsfaktor von Brennwert (Hs) zu Heizwert (Hi) einlesen
        """
        f_ghg, f_pe, f_hs_hi, fuel_type = simulator.get_ghg_pe_conversion_factors(fuel_type)

        heating_sys_electricity_hi_sum, heating_sys_carbon_sum, heating_sys_pe_sum, heating_sys_fossils_hi_sum = simulator.check_heating_sys_electricity_sum(
            sum_of_all_results, f_hs_hi, f_ghg, f_pe)

        heating_sys_hi_sum = simulator.sys_electricity_folssils_sum(
            heating_sys_electricity_hi_sum, heating_sys_fossils_hi_sum)

        heating_fuel_type = fuel_type
        heating_f_ghg = f_ghg
        heating_f_pe = f_pe
        heating_f_hs_hi = f_hs_hi

        """
        HOT WATER
        Assumption: Central DHW-Systems use the same Fuel_type as Heating-Systems, only decentral DHW-Systems might have
        another Fuel-Type.
        """
        fuel_type = simulator.check_if_central_dhw_use_same_fuel_type_as_heating_system(heating_fuel_type)

        f_ghg, f_pe, f_hs_hi, fuel_type = simulator.get_ghg_pe_conversion_factors(fuel_type)

        hot_water_sys_electricity_hi_sum, hot_water_sys_pe_sum, hot_water_sys_carbon_sum, hot_water_sys_fossils_hi_sum = simulator.check_hotwater_sys_electricity_sum(
            sum_of_all_results, f_hs_hi, f_ghg, f_pe)

        hot_water_energy_hi_sum = simulator.sys_electricity_folssils_sum(hot_water_sys_electricity_hi_sum,
                                                                         hot_water_sys_fossils_hi_sum)

        hot_water_fuel_type = fuel_type
        hot_water_f_ghg = f_ghg
        hot_water_f_pe = f_pe
        hot_water_f_hs_hi = f_hs_hi

        """
        Cooling energy
        """
        fuel_type = simulator.choose_cooling_energy_fuel_type()

        f_ghg, f_pe, f_hs_hi, fuel_type = simulator.get_ghg_pe_conversion_factors(fuel_type)

        cooling_sys_electricity_hi_sum, cooling_sys_carbon_sum, cooling_sys_pe_sum, cooling_sys_fossils_hi_sum = simulator.check_cooling_system_elctricity_sum(
            sum_of_all_results, f_hs_hi, f_ghg, f_pe)

        cooling_sys_hi_sum = simulator.cooling_sys_hi_sum(cooling_sys_electricity_hi_sum, cooling_sys_fossils_hi_sum)

        cooling_fuel_type = fuel_type
        cooling_f_ghg = f_ghg
        cooling_f_pe = f_pe
        cooling_f_hs_hi = f_hs_hi

        """
        remaining Electric energy (LightingDemand_sum + Appliance_gains_elt_demand_sum)
        Lighting
        electrical energy for lighting
        """
        fuel_type = 'Electricity grid mix'
        f_ghg, f_pe, f_hs_hi, fuel_type = simulator.get_ghg_pe_conversion_factors(fuel_type)

        lighting_demand_hi_sum = sum_of_all_results.LightingDemand_sum / f_hs_hi  # for kWhHi Final Energy Demand
        lighting_demand_carbon_sum = (lighting_demand_hi_sum * f_ghg) / 1000  # for kg CO2eq
        lighting_demand_pe_sum = lighting_demand_hi_sum * f_pe  # for kWhHs Primary Energy Demand

        appliance_gains_demand_hi_sum = sum_of_all_results.Appliance_gains_elt_demand_sum / f_hs_hi  # for kWhHi Final Energy Demand
        appliance_gains_demand_pe_sum = appliance_gains_demand_hi_sum * f_pe  # for kWhHs Primary Energy Demand
        appliance_gains_demand_carbon_sum = (appliance_gains_demand_hi_sum * f_ghg) / 1000  # for kg CO2eq

        light_appl_fuel_type = fuel_type
        light_appl_f_ghg = f_ghg
        light_appl_f_pe = f_pe
        light_appl_f_hs_hi = f_hs_hi

        """
        Calculation of Carbon Emission related to the entire energy consumption (Heating_Sys_Carbon_sum + 
        Cooling_Sys_Carbon_sum + LightingDemand_Carbon_sum + Appliance_gains_demand_Carbon_sum)
        """
        carbon_sum = heating_sys_carbon_sum + cooling_sys_carbon_sum + lighting_demand_carbon_sum + appliance_gains_demand_carbon_sum + hot_water_sys_carbon_sum

        """
        Calculation of Primary Energy Demand related to the entire energy consumption (Heating_Sys_PE_sum +
         Cooling_Sys_PE_sum + LightingDemand_PE_sum + Appliance_gains_demand_PE_sum + HotWater_Sys_PE_sum)
        """
        pe_sum = heating_sys_pe_sum + cooling_sys_pe_sum + lighting_demand_pe_sum + appliance_gains_demand_pe_sum + hot_water_sys_pe_sum

        """
        Calculation of Final Energy Hi Demand related to the entire energy consumption
        """
        fe_hi_sum = heating_sys_hi_sum + cooling_sys_hi_sum + lighting_demand_hi_sum + appliance_gains_demand_hi_sum + hot_water_energy_hi_sum

        """
        Build Results of a building
        """
        result_output = ResultOutput(simulator.building_object, sum_of_all_results, heating_sys_hi_sum,
                                     heating_sys_electricity_hi_sum, heating_sys_fossils_hi_sum, heating_sys_carbon_sum,
                                     heating_sys_pe_sum, cooling_sys_carbon_sum, cooling_sys_pe_sum,
                                     hot_water_energy_hi_sum, heating_fuel_type, heating_f_ghg, heating_f_pe,
                                     heating_f_hs_hi, hot_water_fuel_type, hot_water_f_ghg, hot_water_f_pe,
                                     hot_water_f_hs_hi, cooling_fuel_type, cooling_f_ghg, cooling_f_pe, cooling_f_hs_hi,
                                     light_appl_fuel_type, light_appl_f_ghg, light_appl_f_pe, light_appl_f_hs_hi,
                                     hot_water_sys_carbon_sum, hot_water_sys_pe_sum, lighting_demand_carbon_sum,
                                     lighting_demand_pe_sum, appliance_gains_demand_carbon_sum,
                                     appliance_gains_demand_pe_sum, carbon_sum, pe_sum, fe_hi_sum, schedule_name,
                                     typ_norm, epw_file_object.file_name)

        # print(result_output.fe_hi_sum)