"""
This class contains the methods that simulate either one building or all buildings
"""
import os.path

from iso_simulator.data_source.datasource import DataSource
from iso_simulator.data_source.datasource_csv import DataSourceCSV
from iso_simulator.building_simulator.simulator import BuildingSimulator
from iso_simulator.building_simulator.all_buildings import SimulateAllBuilding
from iso_simulator.model.results import Result
from iso_simulator.model.ResultOutput import ResultOutput
from iso_simulator.model.building import Building
import time
import concurrent.futures
import multiprocessing
from typing import List
from rich.progress import Progress


class DIBS:
    def __init__(self, datasource: DataSourceCSV):
        """
        This constructor to initialize an instance of the DIBS class
        Args:
            datasource: object which can deal with several data format (csv file, JSON, database, etc...)
        """
        self.datasource = datasource
        self.callback = None

    def set_callback(self, callback_function):
        self.callback = callback_function

    def set_data_source(self, datasource: DataSource):
        self.datasource = datasource

    def calculate_result_of_one_building(self, path: str, user_arguments: List):
        """
        This method simulates the building with the given building_id as parameter
        Args:
            path: The path to the file which contains the building to simulate
            user_arguments: List of user arguments

        Returns:

        """
        time_begin = time.time()

        folder_path = os.path.dirname(path)

        (
            profile_from_norm,
            gains_from_group_values,
            usage_from_norm,
            weather_period,
        ) = user_arguments

        simulator = BuildingSimulator(
            path,
            self.datasource,
            weather_period,
            profile_from_norm,
            gains_from_group_values,
            usage_from_norm,
        )

        t_set_heating_temp = simulator.building_object.t_set_heating

        result, result_output = self.extracted_method_to_simulate_one_building(simulator, t_set_heating_temp)

        simulation_time = time.time() - time_begin

        result_data_frame = simulator.datasource.result_to_pandas_dataframe(
            result_output, user_arguments
        )

        excel_file_name = simulator.building_object.scr_gebaeude_id + ".xlsx"
        with Progress() as progress:
            task = progress.add_task("[cyan]Saving results in Excel file...", total=1)

            start_time = time.time()
            excel_file_path = os.path.join(folder_path, excel_file_name)
            result_data_frame.to_excel(excel_file_path)
            end_time = time.time()
            excel_time = end_time - start_time
            progress.update(task, advance=1)
            progress.update(task, completed=1)

        with Progress() as progress:
            task = progress.add_task("[cyan]Saving results in csv file...", total=1)

            start_time = time.time()
            csv_file_name = simulator.datasource.result_of_all_hours_to_excel(
                folder_path, result, simulator.building_object
            )
            end_time = time.time()
            csv_time = end_time - start_time
            progress.update(task, advance=1)
            progress.update(task, completed=1)

        return (
            result_data_frame,
            simulator.building_object.scr_gebaeude_id,
            simulation_time,
            excel_time,
            csv_time,
            excel_file_name,
            csv_file_name,
        )

    def extracted_method_to_simulate_one_building(self, simulator, t_set_heating_temp):
        result = Result()
        simulator.check_energy_area_and_heating()
        gain_person_and_typ_norm, appliance_gains = simulator.datasource.get_gains(
            simulator.building_object.hk_geb,
            simulator.building_object.uk_geb,
            simulator.profile_from_norm,
            simulator.gains_from_group_values,
        )
        gain_per_person, typ_norm = gain_person_and_typ_norm
        usage_start, usage_end = simulator.get_usage_start_and_end()
        (
            occupancy_schedule,
            schedule_name,
            occupancy_full_usage_hours,
        ) = simulator.get_schedule()
        tek_dhw, tek_name = simulator.get_tek()
        tek_dhw_per_occupancy_full_usage_hour = tek_dhw / occupancy_full_usage_hours
        t_m_prev = simulator.building_object.t_start
        with Progress() as progress:
            task = progress.add_task(
                f"[magenta]Simulating the building with id : {simulator.building_object.scr_gebaeude_id}...",
                total=8760,
            )
            for hour in range(8760):
                simulator.building_object.t_set_heating = t_set_heating_temp
                t_out = simulator.extract_outdoor_temperature(hour)

                altitude, azimuth = simulator.calc_altitude_and_azimuth(hour)

                simulator.building_object.h_ve_adj = (
                    simulator.building_object.calc_h_ve_adj(
                        hour, t_out, usage_start, usage_end
                    )
                )

                t_air = simulator.set_t_air_based_on_hour(hour)

                simulator.calc_solar_gains_for_all_windows(
                    altitude, azimuth, t_air, hour
                )
                simulator.calc_illuminance_for_all_windows(altitude, azimuth, hour)

                occupancy_percent = occupancy_schedule[hour].People
                occupancy = simulator.calc_occupancy(occupancy_schedule, hour)

                simulator.building_object.solve_building_lighting(
                    simulator.calc_sum_illuminance_all_windows(), occupancy_percent
                )
                internal_gains = simulator.calc_gains_from_occupancy_and_appliances(
                    occupancy_schedule,
                    occupancy,
                    gain_per_person,
                    appliance_gains,
                    hour,
                )

                """
                Calculate appliance_gains as part of the internal_gains
                """
                appliance_gains_demand = simulator.calc_appliance_gains_demand(
                    occupancy_schedule, appliance_gains, hour
                )
                """
                Appliance_gains equal the electric energy that appliances use, except for negative appliance_gains of refrigerated counters in trade buildings for food!
                The assumption is: negative appliance_gains come from referigerated counters with heat pumps for which we assume a COP = 2.
                """
                appliance_gains_demand_elt = simulator.get_appliance_gains_elt_demand(
                    occupancy_schedule, appliance_gains, hour
                )
                """
                Calculate energy demand for the time step
                """
                simulator.calc_energy_demand_for_time_step(
                    internal_gains, t_out, t_m_prev
                )
                """
                Calculate hot water usage of the building for the time step with (BuildingInstance.heating_energy
                 / BuildingInstance.heating_demand) represents the Efficiency of the heat generation in the building
                """

                (
                    hot_water_demand,
                    hot_water_energy,
                    hot_water_sys_electricity,
                    hot_water_sys_fossils,
                ) = simulator.calc_hot_water_usage(
                    occupancy_schedule, tek_dhw_per_occupancy_full_usage_hour, hour
                )

                """
                Set the previous temperature for the next time step
                """
                t_m_prev = simulator.building_object.t_m_next
                """
                Append results to the created lists 
                """
                result.append_results(
                    simulator.building_object,
                    simulator.all_windows,
                    hot_water_demand,
                    hot_water_energy,
                    hot_water_sys_electricity,
                    hot_water_sys_fossils,
                    t_out,
                    internal_gains,
                    appliance_gains_demand,
                    appliance_gains_demand_elt,
                    simulator.calc_sum_solar_gains_all_windows(),
                    hour,
                )
                progress.update(task, advance=1)
            progress.stop()
        """
            Some calculations used for the console prints
            """
        sum_of_all_results = result.calc_sum_of_results()
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
        f_ghg, f_pe, f_hs_hi, fuel_type = simulator.get_ghg_pe_conversion_factors(
            fuel_type
        )
        (
            heating_sys_electricity_hi_sum,
            heating_sys_carbon_sum,
            heating_sys_pe_sum,
            heating_sys_fossils_hi_sum,
        ) = simulator.check_heating_sys_electricity_sum(
            sum_of_all_results, f_hs_hi, f_ghg, f_pe
        )
        heating_sys_hi_sum = simulator.sys_electricity_folssils_sum(
            heating_sys_electricity_hi_sum, heating_sys_fossils_hi_sum
        )
        heating_fuel_type = fuel_type
        heating_f_ghg = f_ghg
        heating_f_pe = f_pe
        heating_f_hs_hi = f_hs_hi
        """
            HOT WATER
            Assumption: Central DHW-Systems use the same Fuel_type as Heating-Systems, only decentral DHW-Systems might have
            another Fuel-Type.
            """
        fuel_type = simulator.check_if_central_dhw_use_same_fuel_type_as_heating_system(
            heating_fuel_type
        )
        f_ghg, f_pe, f_hs_hi, fuel_type = simulator.get_ghg_pe_conversion_factors(
            fuel_type
        )
        (
            hot_water_sys_electricity_hi_sum,
            hot_water_sys_pe_sum,
            hot_water_sys_carbon_sum,
            hot_water_sys_fossils_hi_sum,
        ) = simulator.check_hotwater_sys_electricity_sum(
            sum_of_all_results, f_hs_hi, f_ghg, f_pe
        )
        hot_water_energy_hi_sum = simulator.sys_electricity_folssils_sum(
            hot_water_sys_electricity_hi_sum, hot_water_sys_fossils_hi_sum
        )
        hot_water_fuel_type = fuel_type
        hot_water_f_ghg = f_ghg
        hot_water_f_pe = f_pe
        hot_water_f_hs_hi = f_hs_hi
        """
            Cooling energy
            """
        fuel_type = simulator.choose_cooling_energy_fuel_type()
        f_ghg, f_pe, f_hs_hi, fuel_type = simulator.get_ghg_pe_conversion_factors(
            fuel_type
        )
        (
            cooling_sys_electricity_hi_sum,
            cooling_sys_carbon_sum,
            cooling_sys_pe_sum,
            cooling_sys_fossils_hi_sum,
        ) = simulator.check_cooling_system_elctricity_sum(
            sum_of_all_results, f_hs_hi, f_ghg, f_pe
        )
        cooling_sys_hi_sum = simulator.cooling_sys_hi_sum(
            cooling_sys_electricity_hi_sum, cooling_sys_fossils_hi_sum
        )
        cooling_fuel_type = fuel_type
        cooling_f_ghg = f_ghg
        cooling_f_pe = f_pe
        cooling_f_hs_hi = f_hs_hi
        """
            remaining Electric energy (LightingDemand_sum + Appliance_gains_elt_demand_sum)
            Lighting
            electrical energy for lighting
            """
        fuel_type = "Electricity grid mix"
        f_ghg, f_pe, f_hs_hi, fuel_type = simulator.get_ghg_pe_conversion_factors(
            fuel_type
        )
        lighting_demand_hi_sum = (
                sum_of_all_results.LightingDemand_sum / f_hs_hi
        )  # for kWhHi Final Energy Demand
        lighting_demand_carbon_sum = (
                                             lighting_demand_hi_sum * f_ghg
                                     ) / 1000  # for kg CO2eq
        lighting_demand_pe_sum = (
                lighting_demand_hi_sum * f_pe
        )  # for kWhHs Primary Energy Demand
        appliance_gains_demand_hi_sum = (
                sum_of_all_results.Appliance_gains_elt_demand_sum / f_hs_hi
        )  # for kWhHi Final Energy Demand
        appliance_gains_demand_pe_sum = (
                appliance_gains_demand_hi_sum * f_pe
        )  # for kWhHs Primary Energy Demand
        appliance_gains_demand_carbon_sum = (
                                                    appliance_gains_demand_hi_sum * f_ghg
                                            ) / 1000  # for kg CO2eq
        light_appl_fuel_type = fuel_type
        light_appl_f_ghg = f_ghg
        light_appl_f_pe = f_pe
        light_appl_f_hs_hi = f_hs_hi
        """
                Calculation of Carbon Emission related to the entire energy consumption (Heating_Sys_Carbon_sum + 
                Cooling_Sys_Carbon_sum + LightingDemand_Carbon_sum + Appliance_gains_demand_Carbon_sum)
                """
        carbon_sum = (
                heating_sys_carbon_sum
                + cooling_sys_carbon_sum
                + lighting_demand_carbon_sum
                + appliance_gains_demand_carbon_sum
                + hot_water_sys_carbon_sum
        )
        """
                Calculation of Primary Energy Demand related to the entire energy consumption (Heating_Sys_PE_sum +
                 Cooling_Sys_PE_sum + LightingDemand_PE_sum + Appliance_gains_demand_PE_sum + HotWater_Sys_PE_sum)
                """
        pe_sum = (
                heating_sys_pe_sum
                + cooling_sys_pe_sum
                + lighting_demand_pe_sum
                + appliance_gains_demand_pe_sum
                + hot_water_sys_pe_sum
        )
        """
                Calculation of Final Energy Hi Demand related to the entire energy consumption
                """
        fe_hi_sum = (
                heating_sys_hi_sum
                + cooling_sys_hi_sum
                + lighting_demand_hi_sum
                + appliance_gains_demand_hi_sum
                + hot_water_energy_hi_sum
        )
        """
                Build Results of a building
                """
        result_output = self.save_result_output_object(appliance_gains_demand_carbon_sum, appliance_gains_demand_pe_sum,
                                                       carbon_sum, cooling_f_ghg, cooling_f_hs_hi, cooling_f_pe,
                                                       cooling_fuel_type, cooling_sys_carbon_sum, cooling_sys_pe_sum,
                                                       fe_hi_sum, heating_f_ghg, heating_f_hs_hi, heating_f_pe,
                                                       heating_fuel_type, heating_sys_carbon_sum,
                                                       heating_sys_electricity_hi_sum, heating_sys_fossils_hi_sum,
                                                       heating_sys_hi_sum, heating_sys_pe_sum, hot_water_energy_hi_sum,
                                                       hot_water_f_ghg, hot_water_f_hs_hi, hot_water_f_pe,
                                                       hot_water_fuel_type, hot_water_sys_carbon_sum,
                                                       hot_water_sys_pe_sum, light_appl_f_ghg, light_appl_f_hs_hi,
                                                       light_appl_f_pe, light_appl_fuel_type,
                                                       lighting_demand_carbon_sum, lighting_demand_pe_sum, pe_sum,
                                                       schedule_name, simulator, sum_of_all_results, typ_norm)
        return result, result_output

    def save_result_output_object(self, appliance_gains_demand_carbon_sum, appliance_gains_demand_pe_sum, carbon_sum,
                                  cooling_f_ghg, cooling_f_hs_hi, cooling_f_pe, cooling_fuel_type,
                                  cooling_sys_carbon_sum, cooling_sys_pe_sum, fe_hi_sum, heating_f_ghg, heating_f_hs_hi,
                                  heating_f_pe, heating_fuel_type, heating_sys_carbon_sum,
                                  heating_sys_electricity_hi_sum, heating_sys_fossils_hi_sum, heating_sys_hi_sum,
                                  heating_sys_pe_sum, hot_water_energy_hi_sum, hot_water_f_ghg, hot_water_f_hs_hi,
                                  hot_water_f_pe, hot_water_fuel_type, hot_water_sys_carbon_sum, hot_water_sys_pe_sum,
                                  light_appl_f_ghg, light_appl_f_hs_hi, light_appl_f_pe, light_appl_fuel_type,
                                  lighting_demand_carbon_sum, lighting_demand_pe_sum, pe_sum, schedule_name, simulator,
                                  sum_of_all_results, typ_norm):
        result_output = ResultOutput(
            simulator.building_object,
            sum_of_all_results,
            heating_sys_hi_sum,
            heating_sys_electricity_hi_sum,
            heating_sys_fossils_hi_sum,
            heating_sys_carbon_sum,
            heating_sys_pe_sum,
            cooling_sys_carbon_sum,
            cooling_sys_pe_sum,
            hot_water_energy_hi_sum,
            heating_fuel_type,
            heating_f_ghg,
            heating_f_pe,
            heating_f_hs_hi,
            hot_water_fuel_type,
            hot_water_f_ghg,
            hot_water_f_pe,
            hot_water_f_hs_hi,
            cooling_fuel_type,
            cooling_f_ghg,
            cooling_f_pe,
            cooling_f_hs_hi,
            light_appl_fuel_type,
            light_appl_f_ghg,
            light_appl_f_pe,
            light_appl_f_hs_hi,
            hot_water_sys_carbon_sum,
            hot_water_sys_pe_sum,
            lighting_demand_carbon_sum,
            lighting_demand_pe_sum,
            appliance_gains_demand_carbon_sum,
            appliance_gains_demand_pe_sum,
            carbon_sum,
            pe_sum,
            fe_hi_sum,
            schedule_name,
            typ_norm,
            simulator.epw_object.file_name,
        )
        return result_output

    def calculate_result_of_all_buildings(
            self, user_buildings: List[Building], user_arguments: List, index: int
    ) -> tuple[Result, ResultOutput]:
        gwp_pe_factors = self.datasource.get_epw_pe_factors()

        (
            profile_from_norm,
            gains_from_group_values,
            usage_from_norm,
            weather_period,
        ) = user_arguments

        simulator = SimulateAllBuilding(
            self.datasource,
            gwp_pe_factors,
            user_buildings[index],
            weather_period,
            profile_from_norm,
            gains_from_group_values,
            usage_from_norm,
        )

        t_set_heating_temp = user_buildings[index].t_set_heating

        result, result_output = self.extracted_method_to_simulate_one_building(simulator, t_set_heating_temp)

        return result, result_output

    def unpack_results(self, results):
        begin_unpack_time = time.time()
        result, result_output = zip(*results)
        end_unpack_time = time.time()
        return end_unpack_time - begin_unpack_time, result, result_output

    def save_results_of_all_buildings_in_csv_parallel_using_thread_executor(
            self, folder_path: str, buildings, result
    ):
        with Progress() as progress:
            task = progress.add_task("[cyan]Saving results in csv files...", total=1)
            begin_saving_time = time.time()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(
                        self.datasource.result_of_all_hours_to_csv,
                        folder_path,
                        result[index],
                        building,
                    )
                    for index, building in enumerate(buildings)
                ]
                results = [
                    future.result()
                    for future in concurrent.futures.as_completed(futures)
                ]
            end_saving_time = time.time()
            progress.update(task, advance=1)
            progress.update(task, completed=1)
        return end_saving_time - begin_saving_time

    def multi(self, user_buildings, path: str, user_arguments: List):
        folder_path = os.path.dirname(path)

        with multiprocessing.Pool() as pool:
            results = []
            begin = time.time()

            for index, building in enumerate(user_buildings):
                result = pool.apply_async(
                    self.calculate_result_of_all_buildings,
                    (user_buildings, user_arguments, index),
                )
                results.append(result)

            pool.close()
            pool.join()

            results = [result.get() for result in results]
            end = time.time()
            simulation_time = end - begin

            unpack_time, result, result_output = self.unpack_results(results)

            with Progress() as progress:
                begin_final_result = time.time()
                task = progress.add_task(
                    "[cyan]Saving results in Excel file...", total=1
                )
                self.datasource.build_all_results_of_all_buildings(
                    result_output, user_arguments, folder_path
                )
                end_final_result = time.time()
                excel_time = end_final_result - begin_final_result
                progress.update(task, advance=1)
                progress.update(task, completed=1)

        saving_time = (
            self.save_results_of_all_buildings_in_csv_parallel_using_thread_executor(
                folder_path, user_buildings, result
            )
        )
        return simulation_time, excel_time, saving_time, folder_path
