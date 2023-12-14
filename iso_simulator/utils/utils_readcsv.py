import os
import pandas as pd


def read_building_data() -> pd.DataFrame:
    return pd.read_csv(
        'iso_simulator/annualSimulation/SimulationData_Breitenerhebung.csv', sep=';', index_col=False, encoding='utf8')


def read_gwp_pe_factors_data() -> pd.DataFrame:
    return pd.read_csv(
        'iso_simulator/annualSimulation/LCA/Primary_energy_and_emission_factors.csv', sep=';', decimal=',',
        index_col=False, encoding='cp1250', dtype={'Energy Carrier': str, 'Primary Energy Factor GEG   [-]': float,
                                                   'Relation Calorific to Heating Value GEG  [-]': float,
                                                   'GWP spezific to heating value GEG [g/kWh]': float, 'Use': str})
    # df['Energy Carrier'] = df['Energy Carrier'].apply(lambda x: 'None' if x is None else x)


def read_plz_codes_data() -> pd.DataFrame:
    return pd.read_csv(os.path.join(
        'iso_simulator/auxiliary/weather_data/plzcodes.csv'), encoding='latin', dtype={'zipcode': int})


def read_profiles_zuweisungen_data(
        file_path=os.path.join('iso_simulator/auxiliary/norm_profiles/profiles_zuweisungen.csv')) -> pd.DataFrame:
    return pd.read_csv(file_path, sep=';', encoding='latin')


def read_occupancy_schedules_zuweisungen_data() -> pd.DataFrame:
    return pd.read_csv(os.path.join('iso_simulator/auxiliary/occupancy_schedules/occupancy_schedules_zuweisungen.csv'),
                       sep=';', encoding='latin')


def read_schedule_file(schedule_name) -> pd.DataFrame:
    return pd.read_csv(os.path.join('iso_simulator/auxiliary/occupancy_schedules/') + schedule_name + '.csv', sep=';')


def read_weather_data(epwfile_path: str) -> pd.DataFrame:
    return pd.read_csv(
        epwfile_path, skiprows=8, header=None)


def read_vergleichswerte_zuweisung() -> pd.DataFrame:
    return pd.read_csv(os.path.join('iso_simulator/auxiliary/TEKs/TEK_NWG_Vergleichswerte_zuweisung.csv'), sep=';',
                       decimal=',', encoding='cp1250')


def read_tek_nwg_vergleichswerte() -> pd.DataFrame:
    return pd.read_csv(os.path.join('iso_simulator/auxiliary/TEKs/TEK_NWG_Vergleichswerte.csv'), sep=';', decimal=',',
                       index_col=False, encoding='cp1250')

# def read_building_data() -> pd.DataFrame:
#     return pd.read_csv(
#         '../iso_simulator/annualSimulation/SimulationData_Breitenerhebung.csv', sep=';', index_col=False, encoding='utf8')
#
# def read_gwp_pe_factors_data() -> pd.DataFrame:
#     return pd.read_csv(
#             '../iso_simulator/annualSimulation/LCA/Primary_energy_and_emission_factors.csv', sep=';', decimal=',', index_col=False, encoding='cp1250')
#
# def read_plz_codes_data() -> pd.DataFrame:
#     return pd.read_csv(os.path.join(
#             '../iso_simulator/auxiliary/weather_data/plzcodes.csv'), encoding='latin', dtype={'zipcode': int})
#
# def read_profiles_zuweisungen_data(file_path=os.path.join('../iso_simulator/auxiliary/norm_profiles/profiles_zuweisungen.csv')) -> pd.DataFrame:
#     return pd.read_csv(file_path, sep=';', encoding='latin')
#
# def read_occupancy_schedules_zuweisungen_data() -> pd.DataFrame:
#     return pd.read_csv(os.path.join('../iso_simulator/auxiliary/occupancy_schedules/occupancy_schedules_zuweisungen.csv'), sep=';', encoding='latin')
#
# def read_schedule_file(schedule_name) -> pd.DataFrame:
#     return pd.read_csv(os.path.join('../iso_simulator/auxiliary/occupancy_schedules/')+schedule_name+'.csv', sep=';')
#
# def read_weather_data(epwfile_path: str) -> pd.DataFrame:
#     return pd.read_csv(
#             epwfile_path, skiprows=8, header=None)
#
# def read_vergleichswerte_zuweisung() -> pd.DataFrame:
#     return pd.read_csv(os.path.join('../iso_simulator/auxiliary/TEKs/TEK_NWG_Vergleichswerte_zuweisung.csv'), sep = ';', decimal=',', encoding = 'cp1250')
#
# def read_tek_nwg_vergleichswerte() -> pd.DataFrame:
#     return pd.read_csv(os.path.join('../iso_simulator/auxiliary/TEKs/TEK_NWG_Vergleichswerte.csv'), sep = ';', decimal=',', index_col = False, encoding = 'cp1250')
