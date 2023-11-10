"""
Module serves as TEK value returner
"""
# 12.04.2022
__author__ = "Julian Bischof"
__copyright__ = "Copyright 2022, Institut Wohnen und Umwelt"
__credits__ = ""
__license__ = "MIT"
import os
import sys
import pandas as pd
import numpy as np
from .readData import ReadCsvAndConvertToJSON
import logging

  

def getTEK(hk_geb, uk_geb):
    """
    Find TEK values from Teilenergiekennwerte zur Bildung der Vergleichswerte gemäß der Bekanntmachung vom 15.04.2021 zum Gebäudeenergiegesetz (GEG) vom 2020, 
    depending on hk_geb, uk_geb
    
    
    :external input data: ../auxiliary/TEKs/TEK_NWG_Vergleichswerte.csv
    
    
    :param hk_geb: usage type (main category)
    :type hk_geb: string
    :param uk_geb: usage type (subcategory)
    :type uk_geb: string

    :return: df_TEK, TEK_name
    :rtype: DataFrame (with floats), string
    """
    """ -------------------------------------------------------------------------------------------------------------------------------
    This code below replaces the pandas library

    readData: ReadCsvAndConvertToJSON = ReadCsvAndConvertToJSON('../auxiliary/TEKs/TEK_NWG_Vergleichswerte_zuweisung.csv')
    data = readData.read_file()
    logging.info(readData.class_name)
    mapp_file_to_classes = readData.create_dynamic_class(data)

    readData_2: ReadCsvAndConvertToJSON = ReadCsvAndConvertToJSON('../auxiliary/TEKs/TEK_NWG_Vergleichswerte.csv')
    DB_TEKs = readData_2.read_file()
    logging.info(readData_2.class_name)
    mapp_file_to_classes = readData_2.create_dynamic_class(DB_TEKs)

    filtered_objects = [obj for obj in mapp_file_to_classes if obj.TEK_Category == TEK_name]
    
    for zuweisung in mapp_file_to_classes:
        if hk_geb in zuweisung.hk_geb:
            if uk_geb in zuweisung.uk_geb:
                TEK_name = str(zuweisung.schedule_name)
                if filtered_objects:
                    first_object = filtered_objects[0]
                    TEK_dhw = float(first_object.TEK_Warmwasser)
                return TEK_dhw, TEK_name
            else:
                return print('uk_geb unbekannt')
        else:
        return print('hk_geb unbekannt')
    ---------------------------------------------------------------------------------------------------------------------"""

    zuweisungen = pd.read_csv(os.path.join('../auxiliary/TEKs/TEK_NWG_Vergleichswerte_zuweisung.csv'), sep = ';', decimal=',', encoding = 'cp1250')
    
    DB_TEKs = pd.read_csv(os.path.join('../auxiliary/TEKs/TEK_NWG_Vergleichswerte.csv'), sep = ';', decimal=',', index_col = False, encoding = 'cp1250')
    #DB_TEKs.set_index("Gebäudekategorie", inplace=True) # Asigne Row indexes
    #DB_TEKs.set_index("TEK_Category", inplace=True) # Asigne Row indexes
    
    if hk_geb in zuweisungen['hk_geb'].values:
        
        if uk_geb in zuweisungen['uk_geb'].values:
            row = zuweisungen[zuweisungen['uk_geb'] == uk_geb]
            TEK_name = row['TEK'].astype(str)
            TEK_name = TEK_name.iloc[0]
            #print(TEK_name)
            df_TEK = DB_TEKs[DB_TEKs['TEK_Category'] == TEK_name]
            TEK_dhw = df_TEK.iloc[0]['TEK Warmwasser']
            TEK_dhw = TEK_dhw.astype(float)
            #print(ABC)
            
            return TEK_dhw, TEK_name # df_TEK
        
        else: 
            return print('uk_geb unbekannt')
        
    else:
        return print('hk_geb unbekannt')    

