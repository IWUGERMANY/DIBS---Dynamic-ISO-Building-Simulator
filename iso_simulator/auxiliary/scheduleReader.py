"""
Module serves as occupancy profile returner


Portions of this software are copyright of their respective authors and released under the MIT license:
RC_BuildingSimulator, Copyright 2016 Architecture and Building Systems, ETH Zurich
"""
__author__ = "Simon Knoll"
__copyright__ = "Copyright 2020, Institut Wohnen und Umwelt"
__credits__ = "Julian Bischof, Michael Hörner"
__license__ = "MIT"
import os
import pandas as pd

  

def getSchedule(hk_geb, uk_geb):
    """
    Find occupancy schedule from SIA2024, depending on hk_geb, uk_geb
    
    
    :external input data: ../auxiliary/occupancy_schedules/occupancy_schedules_zuweisungen.csv
    
    :param hk_geb: usage type (main category)
    :type hk_geb: string
    :param uk_geb: usage type (subcategory)
    :type uk_geb: string

    :return: df_schedule, schedule_name
    :rtype: DataFrame (with floats), string
    """
    
    zuweisungen = pd.read_csv(os.path.join('../auxiliary/occupancy_schedules/occupancy_schedules_zuweisungen.csv'), sep = ';', encoding = 'latin')

    if hk_geb not in zuweisungen['hk_geb'].values:
        return print('hk_geb unbekannt')
    if uk_geb in zuweisungen['uk_geb'].values:
        row = zuweisungen[zuweisungen['uk_geb'] == uk_geb]
        schedule_name = row['schedule_name'].to_string(index = False).strip()
        df_schedule = pd.read_csv(os.path.join('../auxiliary/occupancy_schedules/')+schedule_name+'.csv', sep = ';')

        return df_schedule, schedule_name

    else: 
        return print('uk_geb unbekannt')    

