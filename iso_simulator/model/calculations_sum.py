class CalculationOfSum:
    """
    the fuel-related final energy sums, f.i. HeatingEnergy_sum, are calculated based upon the superior heating value Hs
    since the corresponding expenditure factors from TEK 9.24 represent the ration of Hs-related final energy to useful energy
    """

    def __init__(self,
                 HeatingDemand_sum: float,
                 HeatingEnergy_sum: float,
                 Heating_Sys_Electricity_sum: float,
                 Heating_Sys_Fossils_sum: float,
                 CoolingDemand_sum: float,
                 CoolingEnergy_sum: float,
                 Cooling_Sys_Electricity_sum: float,
                 Cooling_Sys_Fossils_sum: float,
                 HotWaterDemand_sum: float,
                 HotWaterEnergy_sum: float,
                 HotWater_Sys_Electricity_sum: float,
                 HotWater_Sys_Fossils_sum: float,
                 InternalGains_sum: float,
                 Appliance_gains_demand_sum: float,
                 Appliance_gains_elt_demand_sum: float,
                 LightingDemand_sum: float,
                 SolarGainsSouthWindow_sum: float,
                 SolarGainsEastWindow_sum: float,
                 SolarGainsWestWindow_sum: float,
                 SolarGainsNorthWindow_sum: float,
                 SolarGainsTotal_sum: float
                 ):
        self.HeatingDemand_sum = HeatingDemand_sum
        self.HeatingEnergy_sum = HeatingEnergy_sum
        self.Heating_Sys_Electricity_sum = Heating_Sys_Electricity_sum
        self.Heating_Sys_Fossils_sum = Heating_Sys_Fossils_sum
        self.CoolingDemand_sum = CoolingDemand_sum
        self.CoolingEnergy_sum = CoolingEnergy_sum
        self.Cooling_Sys_Electricity_sum = Cooling_Sys_Electricity_sum
        self.Cooling_Sys_Fossils_sum = Cooling_Sys_Fossils_sum
        self.HotWaterDemand_sum = HotWaterDemand_sum
        self.HotWaterEnergy_sum = HotWaterEnergy_sum
        self.HotWater_Sys_Electricity_sum = HotWater_Sys_Electricity_sum
        self.HotWater_Sys_Fossils_sum = HotWater_Sys_Fossils_sum
        self.InternalGains_sum = InternalGains_sum
        self.Appliance_gains_demand_sum = Appliance_gains_demand_sum
        self.Appliance_gains_elt_demand_sum = Appliance_gains_elt_demand_sum
        self.LightingDemand_sum = LightingDemand_sum
        self.SolarGainsSouthWindow_sum = SolarGainsSouthWindow_sum
        self.SolarGainsEastWindow_sum = SolarGainsEastWindow_sum
        self.SolarGainsWestWindow_sum = SolarGainsWestWindow_sum
        self.SolarGainsNorthWindow_sum = SolarGainsNorthWindow_sum
        self.SolarGainsTotal_sum = SolarGainsTotal_sum
