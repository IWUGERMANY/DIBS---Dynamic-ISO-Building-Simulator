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
from .readData import ReadCsvAndConvertToJSON
import logging

  

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
    
    """ -------------------------------------------------------------------------------------------------------------------------------
    This code below replaces the pandas library

    readData: ReadCsvAndConvertToJSON = ReadCsvAndConvertToJSON('../auxiliary/occupancy_schedules/occupancy_schedules_zuweisungen.csv')
    data = readData.read_file()
    mapp_file_to_classes = readData.create_dynamic_class(data)

    for zuweisung in mapp_file_to_classes:
        if hk_geb in zuweisung.hk_geb:
            if uk_geb in zuweisung.uk_geb:
                schedule_name = zuweisung.schedule_name
                logging.info(schedule_name)
                build_path = os.path.join('../auxiliary/occupancy_schedules/')+schedule_name+'.csv'
                initialize_file_reader = ReadCsvAndConvertToJSON(build_path)
                data = initialize_file_reader.read_file()
                build_schedule_name_classes = initialize_file_reader.create_dynamic_class(data)

                return build_schedule_name_classes, schedule_name
            else:
                return print('uk_geb unbekannt')
        else:
            return print('hk_geb unbekannt')
    ---------------------------------------------------------------------------------------------------------------------------------"""

    # readData: ReadCsvAndConvertToJSON = ReadCsvAndConvertToJSON('../auxiliary/occupancy_schedules/occupancy_schedules_zuweisungen.csv')
    # data = readData.read_file()
    # logging.info(readData.file_name)
    # mapp_file_to_classes = readData.create_dynamic_class(data)

            

    zuweisungen = pd.read_csv(os.path.join('../auxiliary/occupancy_schedules/occupancy_schedules_zuweisungen.csv'), sep = ';', encoding = 'latin')    
    
    if hk_geb in zuweisungen['hk_geb'].values:
        
        if uk_geb in zuweisungen['uk_geb'].values:
            row = zuweisungen[zuweisungen['uk_geb'] == uk_geb]
            schedule_name = row['schedule_name'].to_string(index = False).strip()
            df_schedule = pd.read_csv(os.path.join('../auxiliary/occupancy_schedules/')+schedule_name+'.csv', sep = ';')
            
            return df_schedule, schedule_name
        
        else: 
            return print('uk_geb unbekannt')
        
    else:
        return print('hk_geb unbekannt')    

