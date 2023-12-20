from iso_simulator.model.building import Building
from iso_simulator.model.calculations_sum import CalculationOfSum


class ResultOutput:
    def __init__(self, building: Building, sum_object: CalculationOfSum, heating_sys_hi_sum: float,
                 heating_sys_electricity_hi_sum: float, heating_sys_fossils_hi_sum: float,
                 heating_sys_carbon_sum: float, heating_sys_pe_sum: float, cooling_sys_carbon_sum: float,
                 cooling_sys_pe_sum: float, hot_water_energy_hi_sum: float, heating_fuel_type: str,
                 heating_f_ghg: float, heating_f_pe: float, heating_f_hs_hi: float, hot_water_fuel_type: str,
                 hot_water_f_ghg: float, hot_water_f_pe: float, hot_water_f_hs_hi: float, cooling_fuel_type: str,
                 cooling_f_ghg: float, cooling_f_pe: float, cooling_f_hs_hi: float, light_appl_fuel_type: str,
                 light_appl_f_ghg: float, light_appl_f_pe: float, light_appl_f_hs_hi: float,
                 hot_water_sys_carbon_sum: float, hot_water_sys_pe_sum: float, lighting_demand_carbon_sum: float,
                 lighting_demand_pe_sum: float, appliance_gains_demand_carbon_sum: float,
                 appliance_gains_demand_pe_sum: float, carbon_sum: float, pe_sum: float, fe_hi_sum: float,
                 schedule_name: str, typ_norm: str, epw_filename: str):
        self.building = building
        self.sum_object = sum_object
        self.heating_sys_hi_sum = heating_sys_hi_sum
        self.heating_sys_electricity_hi_sum = heating_sys_electricity_hi_sum
        self.heating_sys_fossils_hi_sum = heating_sys_fossils_hi_sum
        self.heating_sys_carbon_sum = heating_sys_carbon_sum
        self.heating_sys_pe_sum = heating_sys_pe_sum
        self.cooling_sys_carbon_sum = cooling_sys_carbon_sum
        self.cooling_sys_pe_sum = cooling_sys_pe_sum
        self.hot_water_energy_hi_sum = hot_water_energy_hi_sum
        self.heating_fuel_type = heating_fuel_type
        self.heating_f_ghg = heating_f_ghg
        self.heating_f_pe = heating_f_pe
        self.heating_f_hs_hi = heating_f_hs_hi
        self.hot_water_fuel_type = hot_water_fuel_type
        self.hot_water_f_ghg = hot_water_f_ghg
        self.hot_water_f_pe = hot_water_f_pe
        self.hot_water_f_hs_hi = hot_water_f_hs_hi
        self.cooling_fuel_type = cooling_fuel_type
        self.cooling_f_ghg = cooling_f_ghg
        self.cooling_f_pe = cooling_f_pe
        self.cooling_f_hs_hi = cooling_f_hs_hi
        self.light_appl_fuel_type = light_appl_fuel_type
        self.light_appl_f_ghg = light_appl_f_ghg
        self.light_appl_f_pe = light_appl_f_pe
        self.light_appl_f_hs_hi = light_appl_f_hs_hi
        self.hot_water_sys_carbon_sum = hot_water_sys_carbon_sum
        self.hot_water_sys_pe_sum = hot_water_sys_pe_sum
        self.lighting_demand_carbon_sum = lighting_demand_carbon_sum
        self.lighting_demand_pe_sum = lighting_demand_pe_sum
        self.appliance_gains_demand_carbon_sum = appliance_gains_demand_carbon_sum
        self.appliance_gains_demand_pe_sum = appliance_gains_demand_pe_sum
        self.carbon_sum = carbon_sum
        self.pe_sum = pe_sum
        self.fe_hi_sum = fe_hi_sum
        self.schedule_name = schedule_name
        self.typ_norm = typ_norm
        self.epw_filename = epw_filename

    def calc_heating_demand(self):
        return self.sum_object.HeatingDemand_sum / self.building.energy_ref_area

    def calc_heating_energy(self):
        return self.sum_object.HeatingEnergy_sum / self.building.energy_ref_area

    def calc_heating_sys_electricity(self):
        return self.sum_object.Heating_Sys_Electricity_sum / self.building.energy_ref_area

    def calc_heating_sys_fossils(self):
        return self.sum_object.Heating_Sys_Fossils_sum / self.building.energy_ref_area

    def calc_heating_sys_gwp(self):
        return self.heating_sys_carbon_sum / self.building.energy_ref_area

    def calc_heating_sys_pe(self):
        return self.heating_sys_pe_sum / self.building.energy_ref_area

    def calc_cooling_demand(self):
        return self.sum_object.CoolingDemand_sum / self.building.energy_ref_area

    def calc_cooling_energy(self):
        return self.sum_object.CoolingEnergy_sum / self.building.energy_ref_area

    def calc_cooling_sys_electricity(self):
        return self.sum_object.Cooling_Sys_Electricity_sum / self.building.energy_ref_area

    def calc_cooling_sys_fossils(self):
        return self.sum_object.Cooling_Sys_Fossils_sum / self.building.energy_ref_area

    def calc_cooling_sys_gwp(self):
        return self.cooling_sys_carbon_sum / self.building.energy_ref_area

    def calc_cooling_sys_pe(self):
        return self.cooling_sys_pe_sum / self.building.energy_ref_area

    def calc_hot_water_demand(self):
        return self.sum_object.HotWaterDemand_sum / self.building.energy_ref_area

    def calc_hot_water_energy(self):
        return self.sum_object.HotWaterEnergy_sum / self.building.energy_ref_area

    def calc_hot_water_sys_gwp(self):
        return self.hot_water_sys_carbon_sum / self.building.energy_ref_area

    def calc_hot_water_sys_pe(self):
        return self.hot_water_sys_pe_sum / self.building.energy_ref_area

    def calc_electricity_demand_total(self):
        return self.sum_object.Heating_Sys_Electricity_sum + self.sum_object.HotWater_Sys_Electricity_sum + self.sum_object.Cooling_Sys_Electricity_sum + self.sum_object.LightingDemand_sum + self.sum_object.Appliance_gains_elt_demand_sum

    def calc_electricity_demand_total_ref(self):
        return self.calc_electricity_demand_total() / self.building.energy_ref_area

    def calc_fossils_demand_total(self):
        return self.sum_object.Heating_Sys_Fossils_sum + self.sum_object.Cooling_Sys_Fossils_sum

    def calc_fossils_demand_total_ref(self):
        return self.calc_fossils_demand_total() / self.building.energy_ref_area

    def calc_lighting_demand_gwp(self):
        return self.lighting_demand_carbon_sum / self.building.energy_ref_area

    def calc_lighting_demand_pe(self):
        return self.lighting_demand_pe_sum / self.building.energy_ref_area

    def calc_appliance_gains_demand_gwp(self):
        return self.appliance_gains_demand_carbon_sum / self.building.energy_ref_area

    def calc_appliance_gains_demand_pe(self):
        return self.appliance_gains_demand_pe_sum / self.building.energy_ref_area

    def calc_gwp(self):
        return self.carbon_sum / self.building.energy_ref_area

    def calc_pe(self):
        return self.pe_sum / self.building.energy_ref_area
