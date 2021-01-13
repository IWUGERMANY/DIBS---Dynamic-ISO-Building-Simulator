"""
Module with 2 functions to get norm data of DIN V 18599 / SIA:2024


Portions of this software are copyright of their respective authors and released under the MIT license:
RC_BuildingSimulator, Copyright 2016 Architecture and Building Systems, ETH Zurich
"""
__author__ = "Simon Knoll"
__copyright__ = "Copyright 2020, Institut Wohnen und Umwelt"
__credits__ = "Julian Bischof, Michael Hörner"
__license__ = "MIT"



import os
import pandas as pd


def getGains(hk_geb, uk_geb, profile_from_norm, gains_from_group_values):
    """
    Find data from DIN V 18599-10 or SIA2024

    
    :external input data: Assignments [../auxiliary/norm_profiles/profiles_zuweisungen.csv]
    
    :param hk_geb: usage type (main category)
    :type hk_geb: string
    :param uk_geb: usage type (subcategory)
    :type uk_geb: string
    :param profile_from_norm: data source either 18599-10 or SIA2024 [specified in annualSimulation.py]
    :type profile_from_norm: string
    :param gains_from_group_values: group in norm low/medium/high [specified in annualSimulation.py]
    :type gains_from_group_values: string

    :return: gain_per_person, appliance_gains, typ_norm
    :rtype: tuple (float, float, string)
    """
    
    gains_zuweisungen = pd.read_csv(os.path.join('../auxiliary/norm_profiles/profiles_zuweisungen.csv'), sep = ';', encoding = 'latin')
    
    if hk_geb in gains_zuweisungen['hk_geb'].values:
        
        if uk_geb in gains_zuweisungen['uk_geb'].values:
            row = gains_zuweisungen[gains_zuweisungen['uk_geb'] == uk_geb]
            
            if profile_from_norm == 'sia2024':
                typ_norm = row['typ_sia2024'].to_string(index = False).strip()
                gain_per_person = float(row['gain_per_person_sia2024'].to_string(index = False).strip())
                
                if gains_from_group_values == 'low':
                    appliance_gains = float(row['appliance_gains_ziel_sia2024'].to_string(index = False).strip())  
                
                elif gains_from_group_values == 'mid':
                        appliance_gains = float(row['appliance_gains_standard_sia2024'].to_string(index = False).strip())  
                
                elif gains_from_group_values == 'max':    
                        appliance_gains = float(row['appliance_gains_bestand_sia2024'].to_string(index = False).strip())
                        
            elif profile_from_norm == 'din18599': 
                typ_norm = row['typ_18599'].to_string(index = False).strip()
                gain_per_person = float(row['gain_per_person_18599'].to_string(index = False).strip())
                
                if gains_from_group_values == 'low':
                    appliance_gains = float(row['appliance_gains_tief_18599'].to_string(index = False).strip())
                    
                elif gains_from_group_values == 'mid':
                        appliance_gains = float(row['appliance_gains_mittel_18599'].to_string(index = False).strip())
                    
                elif gains_from_group_values == 'max':  
                        appliance_gains = float(row['appliance_gains_hoch_18599'].to_string(index = False).strip())

        return gain_per_person, appliance_gains, typ_norm
    
    
    
def getUsagetime(hk_geb, uk_geb, usage_from_norm):
    """
    Find building's usage time DIN 18599-10 or SIA2024

    
    :external input data: Assignments [../auxiliary/norm_profiles/profiles_zuweisungen.csv]
        
    :param hk_geb: usage type (main category)
    :type hk_geb: string
    :param uk_geb: usage type (subcategory)
    :type uk_geb: string
    :param usage_from_norm: data source either 18599-10 or SIA2024 [specified in annualSimulation.py]
    :type usage_from_norm: string

    :return: usage_start, usage_end
    :rtype: tuple (float, float)
    """
    
    gains_zuweisungen = pd.read_csv(os.path.join('../auxiliary/norm_profiles/profiles_zuweisungen.csv'), sep = ';', encoding = 'latin')
    
    if hk_geb in gains_zuweisungen['hk_geb'].values:
        
        if uk_geb in gains_zuweisungen['uk_geb'].values:
            row = gains_zuweisungen[gains_zuweisungen['uk_geb'] == uk_geb]
            
            if usage_from_norm == 'sia2024':    
                usage_start = int(row['usage_start_sia2024'].to_string(index = False).strip())    
                usage_end = int(row['usage_end_sia2024'].to_string(index = False).strip())    
                
            elif usage_from_norm == 'din18599': 
                usage_start = int(row['usage_start_18599'].to_string(index = False).strip())  
                usage_end = int(row['usage_end_18599'].to_string(index = False).strip())  
                
        else: 
            raise ValueError('Something went wrong with the function getUsagetime()')      
            
        return usage_start, usage_end
                