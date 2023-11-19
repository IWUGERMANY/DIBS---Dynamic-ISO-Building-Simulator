from typing import List


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


    """

    def __init__(self):
        
        self.HeatingDemand = []  
        self.HeatingEnergy = []
        self.Heating_Sys_Electricity = []
        self.Heating_Sys_Fossils = []
        self.CoolingDemand = []  
        self.CoolingEnergy = []
        self.Cooling_Sys_Electricity = []
        self.Cooling_Sys_Fossils = []
        self.HotWaterDemand = [] 
        self.HotWaterEnergy = [] 
        self.HotWater_Sys_Electricity = [] 
        self.HotWater_Sys_Fossils = [] 
        self.TempAir = []
        self.OutsideTemp = []
        self.LightingDemand = []
        self.InternalGains = []
        self.SolarGainsSouthWindow = []
        self.SolarGainsEastWindow = []
        self.SolarGainsWestWindow = []
        self.SolarGainsNorthWindow = []
        self.SolarGainsTotal = []
        self.DayTime = []
        self.hotwaterdemand = 0
        self.hotwaterenergy = 0
        self.HotWaterSysElectricity = 0
        self.HotWaterSysFossils = 0


class Results: 

    def __init__(self, results: List[Result]):
        self.results = results

