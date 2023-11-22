import sys
import os
import pandas as pd

mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mainPath)


def readBuildingData() -> pd.DataFrame:
    return pd.read_csv(
        'SimulationData_Breitenerhebung.csv', sep=';', index_col=False, encoding='utf8')

def readGWPPEFactorsData() -> pd.DataFrame:
    return pd.read_csv(
            'LCA/Primary_energy_and_emission_factors.csv', sep=';', decimal=',', index_col=False, encoding='cp1250')

def readPlzCodesData() -> pd.DataFrame:
    return pd.read_csv(os.path.join(
            '../auxiliary/weather_data/plzcodes.csv'), encoding='latin', dtype={'zipcode': int})

def readProfilesZuweisungenData(file_path=os.path.join('../auxiliary/norm_profiles/profiles_zuweisungen.csv')) -> pd.DataFrame:
    return pd.read_csv(file_path, sep=';', encoding='latin')

def readOccupancySchedulesZuweisungenData() -> pd.DataFrame:
    return pd.read_csv(os.path.join('../auxiliary/occupancy_schedules/occupancy_schedules_zuweisungen.csv'), sep=';', encoding='latin')

def readScheduleFile(schedule_name) -> pd.DataFrame:
    return pd.read_csv(os.path.join('../auxiliary/occupancy_schedules/')+schedule_name+'.csv', sep=';')