from typing import List
from iso_simulator.model.building import Building
from iso_simulator.model.calculations_sum import CalculationOfSum
from iso_simulator.model.window import Window


class Result:
    """

    This class contains the result for the calculation of a building

    Args:
    
        heating_demand (List[float]): Space heating demand of the building
        heating_energy (List[float]): Total exergy consumed (electricity + fossils) for heating
        heating_sys_electricity (List[float]): Hating electricity consumption
        heating_sys_fossils (List[float]): Hating fossil fuel consumption
        cooling_demand (List[float]): Space cooling demand of the building
        cooling_energy (List[float]): Total exergy consumed (electricity + fossils) for cooling
        cooling_sys_electricity (List[float]): Electricity consumption from cooling
        cooling_sys_fossils (List[float]): Fossil fuel consumption from cooling
        hotwater_demand (List[float]): Hot water demand of the building
        hotwater_energy (List[float]): 
        hotwater_sys_electricity (List[float]):
        hotwater_sys_fossils (List[float]):
        temp_air (List[float]): Temperature of the air
        outside_temp (List[float]): Temperature of the outside air
        lighting_demand (List[float]): Lighting Energy Required for the timestep
        internal_gains (List[float]): Internal Heat Gains [W]
        solar_gains_south_window (List[float]): 
        solar_gains_east_window (List[float]): 
        solar_gains_west_window (List[float]): 
        solar_gains_north_window (List[float]): 
        solar_gains_total (List[float]):
        day_time: 
        hotwaterdemand:
        hotwaterenergy: 
        hot)water_sys_electricity:
        hot_water_sys_fossils:

    """

    def __init__(self):
        self.heating_demand = []
        self.heating_energy = []
        self.heating_sys_electricity = []
        self.heating_sys_fossils = []
        self.cooling_demand = []
        self.cooling_energy = []
        self.cooling_sys_electricity = []
        self.cooling_sys_fossils = []
        self.all_hot_water_demand = []
        self.all_hot_water_energy = []
        self.hot_water_sys_electricity = []
        self.hot_water_sys_fossils = []
        self.temp_air = []
        self.outside_temp = []
        self.lighting_demand = []
        self.internal_gains = []
        self.solar_gains_south_window = []
        self.solar_gains_east_window = []
        self.solar_gains_west_window = []
        self.solar_gains_north_window = []
        self.solar_gains_total = []
        self.DayTime = []
        # self.hot_water_demand = 0
        # self.hot_water_energy = 0
        # self.HotWaterSysElectricity = 0
        # self.HotWaterSysFossils = 0
        self.appliance_gains_demand = []
        self.appliance_gains_elt_demand = []

    def append_results(self, building: Building, all_windows: List[Window], hot_water_demand: float,
                       hot_water_energy: float, hot_water_sys_electricity: float, hot_water_sys_fossils: float,
                       t_out: float,
                       internal_gains: float, appliance_gains_demand: float,
                       appliance_gains_elt_demand: float, solar_gains_all_windows: float, hour: int) -> None:
        self.heating_demand.append(building.heating_demand)
        self.heating_energy.append(building.heating_energy)
        self.heating_sys_electricity.append(building.heating_sys_electricity)
        self.heating_sys_fossils.append(building.heating_sys_fossils)
        self.cooling_demand.append(building.cooling_demand)
        self.cooling_energy.append(building.cooling_energy)
        self.cooling_sys_electricity.append(building.cooling_sys_electricity)
        self.cooling_sys_fossils.append(building.cooling_sys_fossils)
        self.all_hot_water_demand.append(hot_water_demand)
        self.all_hot_water_energy.append(hot_water_energy)
        self.hot_water_sys_electricity.append(hot_water_sys_electricity)
        self.hot_water_sys_fossils.append(hot_water_sys_fossils)
        self.temp_air.append(building.t_air)
        self.outside_temp.append(t_out)
        self.lighting_demand.append(building.lighting_demand)
        self.internal_gains.append(internal_gains)
        self.solar_gains_south_window.append(all_windows[0].solar_gains)
        self.solar_gains_east_window.append(all_windows[1].solar_gains)
        self.solar_gains_west_window.append(all_windows[2].solar_gains)
        self.solar_gains_north_window.append(all_windows[3].solar_gains)
        self.solar_gains_total.append(solar_gains_all_windows)
        self.DayTime.append(hour % 24)
        self.appliance_gains_demand.append(appliance_gains_demand)
        self.appliance_gains_elt_demand.append(appliance_gains_elt_demand)

    def calc_sum_of_results(self) -> CalculationOfSum:
        heating_demand_sum = sum(self.heating_demand) / 1000
        heating_energy_sum = sum(self.heating_energy) / 1000
        heating_sys_electricity_sum = sum(self.heating_sys_electricity) / 1000
        heating_sys_fossils_sum = sum(self.heating_sys_fossils) / 1000
        cooling_demand_sum = sum(self.cooling_demand) / 1000
        cooling_energy_sum = sum(self.cooling_energy) / 1000
        cooling_sys_electricity_sum = sum(self.cooling_sys_electricity) / 1000
        cooling_sys_fossils_sum = sum(self.cooling_sys_fossils) / 1000
        hot_water_demand_sum = sum(self.all_hot_water_demand) / 1000
        hot_water_energy_sum = sum(self.all_hot_water_energy) / 1000
        hot_water_sys_electricity_sum = sum(self.hot_water_sys_electricity) / 1000
        hot_water_sys_fossils_sum = sum(self.hot_water_sys_fossils) / 1000
        internal_gains_sum = sum(self.internal_gains) / 1000
        appliance_gains_demand_sum = sum(self.appliance_gains_demand) / 1000
        appliance_gains_elt_demand_sum = sum(self.appliance_gains_elt_demand) / 1000
        lighting_demand_sum = sum(self.lighting_demand) / 1000
        solar_gains_south_window_sum = sum(self.solar_gains_south_window) / 1000
        solar_gains_east_window_sum = sum(self.solar_gains_east_window) / 1000
        solar_gains_west_window_sum = sum(self.solar_gains_west_window) / 1000
        solar_gains_north_window_sum = sum(self.solar_gains_north_window) / 1000
        solar_gains_total_sum = sum(self.solar_gains_total) / 1000

        return CalculationOfSum(heating_demand_sum, heating_energy_sum, heating_sys_electricity_sum,
                                heating_sys_fossils_sum, cooling_demand_sum, cooling_energy_sum,
                                cooling_sys_electricity_sum, cooling_sys_fossils_sum, hot_water_demand_sum,
                                hot_water_energy_sum, hot_water_sys_electricity_sum, hot_water_sys_fossils_sum,
                                internal_gains_sum, appliance_gains_demand_sum, appliance_gains_elt_demand_sum,
                                lighting_demand_sum, solar_gains_south_window_sum, solar_gains_east_window_sum,
                                solar_gains_west_window_sum, solar_gains_north_window_sum, solar_gains_total_sum)
