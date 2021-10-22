"""
Dynamic ISO Building Simulator (DIBS)

HOW TO USE

:: Install packages: pandas, numpy, namedlist and geopy 
:: Simulate either 'Tiefenerhebung' or 'Breitenerhebung' 
:: Specify in --> WhatToSimulate
:: Run Simulation
:: Results are stored in ./results/


Portions of this software are copyright of their respective authors and released under the MIT license:
RC_BuildingSimulator, Copyright 2016 Architecture and Building Systems, ETH Zurich

author: "Simon Knoll, Julian Bischof, Michael Hörner "
copyright: "Copyright 2021, Institut Wohnen und Umwelt"
license: "MIT"

"""
__author__ = "Simon Knoll, Julian Bischof, Michael Hörner "
__copyright__ = "Copyright 2021, Institut Wohnen und Umwelt"
__license__ = "MIT"


# Import packages
import sys
import os

# Set root folder one level up
mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mainPath)

# Import more packages
import numpy as np
import pandas as pd

# Import modules
from namedlist import namedlist
from building_physics import Building  
import supply_system
import emission_system
from radiation import Location
from radiation import Window
from auxiliary import scheduleReader
from auxiliary import normReader
 
    
# Create dictionary to store final DataFrames of the buildings
dict_of_results = {}
list_of_summary = []
  
# WhatToSimulate
# Read data with all the buildings from csv file    
# building_data = pd.read_csv('SimulationData_Tiefenerhebung.csv', sep = ';', index_col = False, encoding = 'utf8') 
building_data = pd.read_csv('SimulationData_Breitenerhebung.csv', sep = ';', index_col = False, encoding = 'utf8') 

# Create namedlist of building_data for further iterations
def iterate_namedlist(building_data):
    Row = namedlist('Gebaeude', building_data.columns)
    for row in building_data.itertuples():
        yield Row(*row[1:])

namedlist_of_buildings  = list(iterate_namedlist(building_data))   
        
# Outer loop: Iterate over all buildings in namedlist_of_buildings       
for iteration, i_gebaeudeparameter in enumerate(namedlist_of_buildings):
    

    # Empty Lists to store data
    HeatingDemand = []  
    HeatingEnergy = []
    Heating_Sys_Electricity = []
    Heating_Sys_Fossils = []
    CoolingDemand = []  
    CoolingEnergy = []
    Cooling_Sys_Electricity = []
    Cooling_Sys_Fossils = []
    TempAir = []
    OutsideTemp = []
    LightingDemand = []
    InternalGains = []
    SolarGainsSouthWindow = []
    SolarGainsEastWindow = []
    SolarGainsWestWindow = []
    SolarGainsNorthWindow = []
    SolarGainsTotal = []
    DayTime = []
    
               
    # Initialise an instance of the building
    BuildingInstance = Building(scr_gebaeude_id = i_gebaeudeparameter.scr_gebaeude_id,
                                plz = i_gebaeudeparameter.plz,
                                hk_geb = i_gebaeudeparameter.hk_geb,
                                uk_geb = i_gebaeudeparameter.uk_geb,
                                max_occupancy = i_gebaeudeparameter.max_occupancy,
                                wall_area_og = i_gebaeudeparameter.wall_area_og,
                                wall_area_ug = i_gebaeudeparameter.wall_area_ug,
                                window_area_north = i_gebaeudeparameter.window_area_north,
                                window_area_east = i_gebaeudeparameter.window_area_east,
                                window_area_south = i_gebaeudeparameter.window_area_south,
                                window_area_west = i_gebaeudeparameter.window_area_west,
                                roof_area = i_gebaeudeparameter.roof_area,
                                net_room_area = i_gebaeudeparameter.net_room_area,
                                base_area = i_gebaeudeparameter.base_area,
                                energy_ref_area = i_gebaeudeparameter.energy_ref_area,
                                building_height = i_gebaeudeparameter.building_height,      
                                lighting_load = i_gebaeudeparameter.lighting_load,
                                lighting_control = i_gebaeudeparameter.lighting_control,
                                lighting_utilisation_factor = i_gebaeudeparameter.lighting_utilisation_factor,
                                lighting_maintenance_factor = i_gebaeudeparameter.lighting_maintenance_factor,
                                glass_solar_transmittance = i_gebaeudeparameter.glass_solar_transmittance,
                                glass_solar_shading_transmittance = i_gebaeudeparameter.glass_solar_shading_transmittance,
                                glass_light_transmittance = i_gebaeudeparameter.glass_light_transmittance,
                                u_windows = i_gebaeudeparameter.u_windows,
                                u_walls = i_gebaeudeparameter.u_walls,
                                u_roof = i_gebaeudeparameter.u_roof,
                                u_base = i_gebaeudeparameter.u_base,
                                temp_adj_base = i_gebaeudeparameter.temp_adj_base,
                                temp_adj_walls_ug = i_gebaeudeparameter.temp_adj_walls_ug,
                                ach_inf = i_gebaeudeparameter.ach_inf,
                                ach_win = i_gebaeudeparameter.ach_win,
                                ach_vent = i_gebaeudeparameter.ach_vent,
                                heat_recovery_efficiency = i_gebaeudeparameter.heat_recovery_efficiency,
                                thermal_capacitance = i_gebaeudeparameter.thermal_capacitance,
                                t_start = i_gebaeudeparameter.t_start,
                                t_set_heating = i_gebaeudeparameter.t_set_heating,
                                t_set_cooling = i_gebaeudeparameter.t_set_cooling,
                                night_flushing_flow = i_gebaeudeparameter.night_flushing_flow,
                                max_cooling_energy_per_floor_area = i_gebaeudeparameter.max_cooling_energy_per_floor_area,
                                max_heating_energy_per_floor_area = i_gebaeudeparameter.max_heating_energy_per_floor_area,
                                heating_supply_system = getattr(supply_system, i_gebaeudeparameter.heating_supply_system),  
                                cooling_supply_system = getattr(supply_system, i_gebaeudeparameter.cooling_supply_system),
                                heating_emission_system = getattr(emission_system, i_gebaeudeparameter.heating_emission_system),
                                cooling_emission_system = getattr(emission_system, i_gebaeudeparameter.cooling_emission_system))
    
    # If there's no heated area (energy_ref_area == -8) or no heating supply system (heating_supply_system == 'NoHeating')
    # no heating demand can be calculated. In this case skip calculation and proceed with next building.
    if (i_gebaeudeparameter.energy_ref_area == -8) | (i_gebaeudeparameter.heating_supply_system == 'NoHeating'):
        print('Building ' + str(i_gebaeudeparameter.scr_gebaeude_id) + ' not heated')
        continue
    else: 
        pass
    

    # Initialize the buildings location with a weather file from the nearest weather station depending on the plz
    getEPWFile_list = Location.getEPWFile(BuildingInstance.plz)
    epw_filename = getEPWFile_list[0]                
    building_location = Location(epwfile_path = os.path.join(mainPath, 'auxiliary/weather_data', epw_filename))

    # Distance from weather station to the building
    distance = getEPWFile_list[2] 

    # Extract coordinates of that weather station. Necessary for calc_sun_position()
    latitude_station = getEPWFile_list[1][0]      
    longitude_station = getEPWFile_list[1][1]     
                                                 
    # Define windows for each compass direction
    SouthWindow = Window(azimuth_tilt = 0, alititude_tilt = 90, 
                         glass_solar_transmittance = BuildingInstance.glass_solar_transmittance,
                         glass_solar_shading_transmittance = BuildingInstance.glass_solar_shading_transmittance,
                         glass_light_transmittance = BuildingInstance.glass_light_transmittance, 
                         area = BuildingInstance.window_area_south) 
    EastWindow = Window(azimuth_tilt = 90, alititude_tilt = 90, 
                        glass_solar_transmittance = BuildingInstance.glass_solar_transmittance,
                        glass_solar_shading_transmittance = BuildingInstance.glass_solar_shading_transmittance,
                        glass_light_transmittance = BuildingInstance.glass_light_transmittance, 
                        area = BuildingInstance.window_area_east)
    WestWindow = Window(azimuth_tilt = 180, alititude_tilt = 90, 
                        glass_solar_transmittance = BuildingInstance.glass_solar_transmittance,
                        glass_solar_shading_transmittance = BuildingInstance.glass_solar_shading_transmittance,
                        glass_light_transmittance = BuildingInstance.glass_light_transmittance, 
                        area = BuildingInstance.window_area_west) 
    NorthWindow = Window(azimuth_tilt = 270, alititude_tilt = 90, 
                         glass_solar_transmittance = BuildingInstance.glass_solar_transmittance,
                         glass_solar_shading_transmittance = BuildingInstance.glass_solar_shading_transmittance,
                         glass_light_transmittance = BuildingInstance.glass_light_transmittance, 
                         area = BuildingInstance.window_area_north)  
    
    
    # Get information from DIN V 18599-10 or SIA 2024 for gain_per_person and appliance_gains depending on 
    # hk_geb, uk_geb
    # Assignments see Excel/CSV-File in /auxiliary/norm_profiles/profiles_DIN18599_SIA2024
    din = 'din18599'
    sia = 'sia2024'
    low_values = 'low'
    mid_values = 'mid'
    max_values = 'max'
    
    profile_from_norm = din                   # Choose here where to pick data from 
    gains_from_group_values = mid_values      # Choose here here between low, mid or max values
    gain_per_person, appliance_gains, typ_norm = normReader.getGains(BuildingInstance.hk_geb, BuildingInstance.uk_geb, profile_from_norm, gains_from_group_values)
    
    # Get usage time of the specific building from DIN V 18599-10 or SIA2024
    usage_from_norm = sia
    usage_start, usage_end = normReader.getUsagetime(BuildingInstance.hk_geb, BuildingInstance.uk_geb, usage_from_norm)    
    
    # Read specific occupancy schedule
    # Assignments see Excel/CSV-File in /auxiliary/occupancy_schedules/
    occupancy_schedule, schedule_name = scheduleReader.getSchedule(BuildingInstance.hk_geb, BuildingInstance.uk_geb)
      
   
    # Starting temperature of the building. Set to t_start
    t_m_prev = BuildingInstance.t_start
    
    
    ## Inner Loop: Loop through all 8760 hours of the year
    for hour in range(8760):
        
        # Initialize t_set_heating at the beginning of each time step, due to BuildingInstance.t_set_heating = 0 if night flushing is active
        # (Also see below)
        BuildingInstance.t_set_heating = i_gebaeudeparameter.t_set_heating      
                
        # Extract the outdoor temperature in building_location for that hour from weather_data
        t_out = building_location.weather_data['drybulb_C'][hour]
        
        # Call calc_sun_position(). Depending on latitude, longitude, year and hour - Independent from epw weather_data
        Altitude, Azimuth = building_location.calc_sun_position(
            latitude_deg = latitude_station, longitude_deg = longitude_station, year=building_location.weather_data['year'][hour], hoy=hour)
        
        # Calculate H_ve_adj, See building_physics for details
        BuildingInstance.h_ve_adj = BuildingInstance.calc_h_ve_adj(hour, t_out, usage_start, usage_end)
        
        # Set t_set_heating = 0 for the time step, otherwise the heating system heats up during night flushing is on
        # BuildingInstance.t_set_heating = 0
        

        
        # Define t_air for calc_solar_gains(). Starting condition (hour==0) necessary for first time step  
        if hour == 0:
            t_air = BuildingInstance.t_set_heating
        else: 
            t_air = BuildingInstance.t_air
            
        # Calculate solar gains and illuminance through each window    
        SouthWindow.calc_solar_gains(sun_altitude = Altitude, sun_azimuth = Azimuth,
                                     normal_direct_radiation=building_location.weather_data[
                                         'dirnorrad_Whm2'][hour],
                                     horizontal_diffuse_radiation = building_location.weather_data['difhorrad_Whm2'][hour], 
                                     t_air = t_air, hour = hour)
    
        SouthWindow.calc_illuminance(sun_altitude = Altitude, sun_azimuth = Azimuth,
                                     normal_direct_illuminance=building_location.weather_data[
                                         'dirnorillum_lux'][hour],
                                     horizontal_diffuse_illuminance = building_location.weather_data['difhorillum_lux'][hour])
        
        EastWindow.calc_solar_gains(sun_altitude = Altitude, sun_azimuth = Azimuth,
                                     normal_direct_radiation = building_location.weather_data[
                                         'dirnorrad_Whm2'][hour],
                                     horizontal_diffuse_radiation = building_location.weather_data['difhorrad_Whm2'][hour], 
                                     t_air = t_air, hour = hour)
    
        EastWindow.calc_illuminance(sun_altitude = Altitude, sun_azimuth = Azimuth,
                                     normal_direct_illuminance = building_location.weather_data[
                                         'dirnorillum_lux'][hour],
                                     horizontal_diffuse_illuminance=building_location.weather_data['difhorillum_lux'][hour])
        
        WestWindow.calc_solar_gains(sun_altitude = Altitude, sun_azimuth = Azimuth,
                                     normal_direct_radiation = building_location.weather_data[
                                         'dirnorrad_Whm2'][hour],
                                     horizontal_diffuse_radiation=building_location.weather_data['difhorrad_Whm2'][hour], 
                                     t_air = t_air, hour = hour)
    
        WestWindow.calc_illuminance(sun_altitude = Altitude, sun_azimuth = Azimuth,
                                     normal_direct_illuminance = building_location.weather_data[
                                         'dirnorillum_lux'][hour],
                                     horizontal_diffuse_illuminance=building_location.weather_data['difhorillum_lux'][hour])
        
        NorthWindow.calc_solar_gains(sun_altitude = Altitude, sun_azimuth = Azimuth,
                                     normal_direct_radiation = building_location.weather_data[
                                         'dirnorrad_Whm2'][hour],
                                     horizontal_diffuse_radiation=building_location.weather_data['difhorrad_Whm2'][hour], 
                                     t_air = t_air, hour = hour)
    
        NorthWindow.calc_illuminance(sun_altitude = Altitude, sun_azimuth = Azimuth,
                                     normal_direct_illuminance = building_location.weather_data[
                                         'dirnorillum_lux'][hour],
                                     horizontal_diffuse_illuminance=building_location.weather_data['difhorillum_lux'][hour])
        
        # Occupancy for the time step
        occupancy = occupancy_schedule.loc[hour, 'People'] * BuildingInstance.max_occupancy
        
        # Calculate the lighting of the building for the time step
        BuildingInstance.solve_building_lighting(illuminance=
                                       SouthWindow.transmitted_illuminance +
                                       EastWindow.transmitted_illuminance +
                                       WestWindow.transmitted_illuminance +
                                       NorthWindow.transmitted_illuminance, 
                                       occupancy=occupancy)
    
        # Calculate gains from occupancy and appliances
        internal_gains = occupancy * gain_per_person + \
            appliance_gains * occupancy_schedule.loc[hour, 'Appliances'] * BuildingInstance.energy_ref_area + \
            BuildingInstance.lighting_demand
            
        # Calculate appliance_gains as part of the internal_gains
        Appliance_gains_demand = appliance_gains * occupancy_schedule.loc[hour, 'Appliances'] * BuildingInstance.energy_ref_area
        
            
        # Calculate energy demand for the time step             
        BuildingInstance.solve_building_energy(internal_gains=internal_gains,
                                     solar_gains=
                                     SouthWindow.solar_gains + 
                                     EastWindow.solar_gains + 
                                     WestWindow.solar_gains + 
                                     NorthWindow.solar_gains,
                                     t_out=t_out, t_m_prev=t_m_prev)
    
    
        # Set the previous temperature for the next time step
        t_m_prev = BuildingInstance.t_m_next
                
        # Append results to the created lists  
        HeatingDemand.append(BuildingInstance.heating_demand)
        HeatingEnergy.append(BuildingInstance.heating_energy)
        Heating_Sys_Electricity.append(BuildingInstance.heating_sys_electricity)
        Heating_Sys_Fossils.append(BuildingInstance.heating_sys_fossils)
        CoolingDemand.append(BuildingInstance.cooling_demand)
        CoolingEnergy.append(BuildingInstance.cooling_energy)
        Cooling_Sys_Electricity.append(BuildingInstance.cooling_sys_electricity)
        Cooling_Sys_Fossils.append(BuildingInstance.cooling_sys_fossils)
        TempAir.append(BuildingInstance.t_air)
        OutsideTemp.append(t_out)
        LightingDemand.append(BuildingInstance.lighting_demand)
        InternalGains.append(internal_gains)
        SolarGainsSouthWindow.append(SouthWindow.solar_gains)
        SolarGainsEastWindow.append(EastWindow.solar_gains)
        SolarGainsWestWindow.append(WestWindow.solar_gains)
        SolarGainsNorthWindow.append(NorthWindow.solar_gains)
        SolarGainsTotal.append(SouthWindow.solar_gains+EastWindow.solar_gains+WestWindow.solar_gains+NorthWindow.solar_gains)
        DayTime.append(hour%24)
        
            
    # DataFrame with hourly results of specific building 
    hourlyResults = pd.DataFrame({
        'HeatingDemand': HeatingDemand,
        'HeatingEnergy': HeatingEnergy,
        'Heating_Sys_Electricity': Heating_Sys_Electricity,
        'Heating_Sys_Fossils': Heating_Sys_Fossils,
        'CoolingDemand': CoolingDemand,
        'CoolingEnergy': CoolingEnergy,
        'Cooling_Sys_Electricity': Cooling_Sys_Electricity,
        'Cooling_Sys_Fossils': Cooling_Sys_Fossils,
        'IndoorAirTemperature': TempAir,
        'OutsideTemperature':  OutsideTemp,
        'LightingDemand': LightingDemand,
        'InternalGains': InternalGains,
        'Appliance_gains_demand': Appliance_gains_demand,
        'SolarGainsSouthWindow': SolarGainsSouthWindow,
        'SolarGainsEastWindow': SolarGainsEastWindow,
        'SolarGainsWestWindow': SolarGainsWestWindow,
        'SolarGainsNorthWindow': SolarGainsNorthWindow,
        'SolarGainsTotal': SolarGainsTotal,
        'Daytime': DayTime, 
        })
    
    # Count iteration (amount of buildings), add GebäudeID to the DataFrame and put 
    # DataFrame to the dictionary (dict_of_results)
    hourlyResults['iteration'] = iteration
    hourlyResults['GebäudeID'] = i_gebaeudeparameter.scr_gebaeude_id
    dict_of_results[i_gebaeudeparameter.scr_gebaeude_id] = hourlyResults.copy()
    
    
    # Some calculations used for the console prints
    HeatingDemand_sum = hourlyResults.HeatingDemand.sum()/1000
    HeatingEnergy_sum = hourlyResults.HeatingEnergy.sum()/1000
    Heating_Sys_Electricity_sum = hourlyResults.Heating_Sys_Electricity.sum()/1000
    Heating_Sys_Fossils_sum = hourlyResults.Heating_Sys_Fossils.sum()/1000
    CoolingDemand_sum = hourlyResults.CoolingDemand.sum()/1000
    CoolingEnergy_sum = hourlyResults.CoolingEnergy.sum()/1000
    Cooling_Sys_Electricity_sum = hourlyResults.Cooling_Sys_Electricity.sum()/1000
    Cooling_Sys_Fossils_sum = hourlyResults.Cooling_Sys_Fossils.sum()/1000
    InternalGains_sum = hourlyResults.InternalGains.sum()/1000
    Appliance_gains_demand_sum = hourlyResults.Appliance_gains_demand.sum()/1000
    LightingDemand_sum = hourlyResults.LightingDemand.sum()/1000
    SolarGainsSouthWindow_sum = hourlyResults.SolarGainsSouthWindow.sum()/1000
    SolarGainsEastWindow_sum = hourlyResults.SolarGainsEastWindow.sum()/1000
    SolarGainsWestWindow_sum = hourlyResults.SolarGainsWestWindow.sum()/1000
    SolarGainsNorthWindow_sum = hourlyResults.SolarGainsNorthWindow.sum()/1000
    SolarGainsTotal_sum = hourlyResults.SolarGainsTotal.sum()/1000 
    
    print("# ", iteration)
    print("GebäudeID:", i_gebaeudeparameter.scr_gebaeude_id)
    print("HeatingDemand [kwh]:", HeatingDemand_sum)
    print("HeatingDemand [kwh/m2]:", HeatingDemand_sum/BuildingInstance.energy_ref_area)
    print("HeatingEnergy [kwh]:", HeatingEnergy_sum)
    print("HeatingEnergy [kwh/m2]:", HeatingEnergy_sum/BuildingInstance.energy_ref_area)
    # print("Heating_Sys_Electricity [kwh]:", Heating_Sys_Electricity_sum)
    # print("Heating_Sys_Fossils [kwh]:", Heating_Sys_Fossils_sum)
    print("CoolingDemand [kwh]:", CoolingDemand_sum)
    print("CoolingDemand [kwh/m2]:", CoolingDemand_sum/BuildingInstance.energy_ref_area)
    print("CoolingEnergy [kwh]:", CoolingEnergy_sum)
    print("CoolingEnergy [kwh/m2]:", CoolingEnergy_sum/BuildingInstance.energy_ref_area)
    # print("Cooling_Sys_Electricity [kwh]:", Cooling_Sys_Electricity_sum)
    # print("Cooling_Sys_Fossils [kwh]:", Cooling_Sys_Fossils_sum)
    print("LightingDemand [kwh]:", LightingDemand_sum)
    print("Appliance_gains_demand [kWh]:", Appliance_gains_demand_sum)
    print("InternalGains [kwh]:", InternalGains_sum)
    # print("SolarGainsSouthWindow [kwh]:", SolarGainsSouthWindow_sum)
    # print("SolarGainsEastWindow [kwh]:", SolarGainsEastWindow_sum)
    # print("SolarGainsWestWindow [kwh]:", SolarGainsWestWindow_sum)
    # print("SolarGainsNorthWindow [kwh]:", SolarGainsNorthWindow_sum)
    print("SolarGainsTotal [kwh]:", SolarGainsTotal_sum)
    
    # Summary of building to a separate DataFrame
    annualResults_summary_temp = pd.DataFrame({
                                        'GebäudeID': i_gebaeudeparameter.scr_gebaeude_id,
                                        'EnergyRefArea': BuildingInstance.energy_ref_area,
                                        'HeatingDemand': HeatingDemand_sum,
                                        'HeatingDemand [kwh/m2]': HeatingDemand_sum/BuildingInstance.energy_ref_area,
                                        'HeatingEnergy': HeatingEnergy_sum,
                                        'HeatingEnergy [kwh/m2]': HeatingEnergy_sum/BuildingInstance.energy_ref_area,
                                        'Heating_Sys_Electricity': Heating_Sys_Electricity_sum,
                                        'Heating_Sys_Electricity [kwh/m2]': Heating_Sys_Electricity_sum/BuildingInstance.energy_ref_area,
                                        'Heating_Sys_Fossils': Heating_Sys_Fossils_sum,
                                        'Heating_Sys_Fossils [kwh/m2]': Heating_Sys_Fossils_sum/BuildingInstance.energy_ref_area,
                                        'CoolingDemand': CoolingDemand_sum,
                                        'CoolingDemand [kwh/m2]': CoolingDemand_sum/BuildingInstance.energy_ref_area,
                                        'CoolingEnergy' : CoolingEnergy_sum,
                                        'CoolingEnergy [kwh/m2]': CoolingEnergy_sum/BuildingInstance.energy_ref_area,
                                        'Cooling_Sys_Electricity': Cooling_Sys_Electricity_sum,
                                        'Cooling_Sys_Electricity [kwh/m2]': Cooling_Sys_Electricity_sum/BuildingInstance.energy_ref_area,
                                        'Cooling_Sys_Fossils': Cooling_Sys_Fossils_sum,
                                        'Cooling_Sys_Fossils [kwh/m2]': Cooling_Sys_Fossils_sum/BuildingInstance.energy_ref_area,
                                        'ElectricityDemandTotal': Heating_Sys_Electricity_sum + Cooling_Sys_Electricity_sum + LightingDemand_sum + Appliance_gains_demand_sum, 
                                        'ElectricityDemandTotal [kwh/m2]': (Heating_Sys_Electricity_sum + Cooling_Sys_Electricity_sum + LightingDemand_sum + Appliance_gains_demand_sum)/BuildingInstance.energy_ref_area, 
                                        'FossilsDemandTotal': Heating_Sys_Fossils_sum + Cooling_Sys_Fossils_sum,
                                        'FossilsDemandTotal [kwh/m2]': (Heating_Sys_Fossils_sum + Cooling_Sys_Fossils_sum)/BuildingInstance.energy_ref_area,
                                        'LightingDemand': LightingDemand_sum,
                                        'Appliance_gains_demand': Appliance_gains_demand_sum,
                                        'InternalGains': InternalGains_sum,
                                        'SolarGainsTotal': SolarGainsTotal_sum,
                                        'SolarGainsSouthWindow': SolarGainsSouthWindow_sum,
                                        'SolarGainsEastWindow': SolarGainsEastWindow_sum,
                                        'SolarGainsWestWindow': SolarGainsWestWindow_sum,
                                        'SolarGainsNorthWindow': SolarGainsNorthWindow_sum,
                                        'Gebäudefunktion Hauptkategorie': i_gebaeudeparameter.hk_geb,
                                        'Gebäudefunktion Unterkategorie': i_gebaeudeparameter.uk_geb,
                                        'Profil SIA 2024': [schedule_name],
                                        'Profil 18599-10': [typ_norm],
                                        'EPW-File': [epw_filename],
                                        'HeatingSupplySystem': i_gebaeudeparameter.heating_supply_system,
                                        'CoolingSupplySystem': i_gebaeudeparameter.cooling_supply_system
                                        })  
    # Append DataFrame to list_of_summary
    list_of_summary.append(annualResults_summary_temp)

    # Merge all summary DataFrames and save to disc 
    annualResults_summary = pd.concat(list_of_summary)
    annualResults_summary.to_excel(r'./results/annualResults_summary.xlsx', index = False)


# The function writes DataFrames of dict_of_results to the system (to_excel)    
def save_dfs_dict(dictex):
    for key, val in dictex.items():
        val.to_excel(r'./results/{}.xlsx'.format(str(key)))
      
save_dfs_dict(dict_of_results)
