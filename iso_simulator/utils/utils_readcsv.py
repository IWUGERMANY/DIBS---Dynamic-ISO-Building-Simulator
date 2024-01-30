"""
This file only contains methods that simply read different csv files
"""

import os
import pandas as pd


def read_user_building(path: str):
    """
    This method reads the file which contains the building data to simulate.
    Args:
        path: where the file is located

    Returns:
        building
    Return type:
        Building
    """
    path_parts = path.split("/")
    file_path = os.path.join(*path_parts)

    return pd.read_csv(file_path, sep=";", index_col=False, encoding="utf8")


def read_user_buildings(path: str):
    """
    This method reads the file which contains the building data to simulate.
    Args:
        path: where the file is located

    Returns:
        building
    Return type:
        Building
    """
    path_parts = path.split("/")
    file_path = os.path.join(*path_parts)

    return pd.read_csv(file_path, sep=";", index_col=False, encoding="utf8")


def read_one_building(building_id: str) -> pd.DataFrame | None:
    """
    Searches the building with the given building_id
    Args:
        building_id: building to simulate

    Returns:
        dataframe that contains just the building with the given building_id or None
    """
    df = pd.read_csv(
        "iso_simulator/annualSimulation/SimulationData_Breitenerhebung.csv",
        sep=";",
        index_col=False,
        encoding="utf8",
    )
    return df[df["scr_gebaeude_id"] == building_id]


def read_building_data() -> pd.DataFrame:
    """
    Reads the csv file that contains all building
    Returns:
        dataframe
    """
    return pd.read_csv(
        "iso_simulator/annualSimulation/SimulationData_Breitenerhebung.csv",
        sep=";",
        index_col=False,
        encoding="utf8",
    )


def read_gwp_pe_factors_data() -> pd.DataFrame:
    """
    Reads the csv file Primary_energy_and_emission_factors and replaces in the dataframe nan value with None
    Returns:
        dataframe
    """
    data = pd.read_csv(
        "iso_simulator/annualSimulation/LCA/Primary_energy_and_emission_factors.csv",
        sep=";",
        decimal=",",
        index_col=False,
        encoding="cp1250",
    )
    nan_values = data[data["Energy Carrier"].isna()]
    if not nan_values.empty:
        data["Energy Carrier"].replace({pd.NaT: "None"}, inplace=True)
    return data


def read_plz_codes_data() -> pd.DataFrame:
    """
    Reads the csv file plzcodes
    Returns:
        dataframe
    """
    return pd.read_csv(
        os.path.join("iso_simulator/auxiliary/weather_data/plzcodes.csv"),
        encoding="latin",
        dtype={"zipcode": int},
    )


def read_profiles_zuweisungen_data(
    file_path=os.path.join(
        "iso_simulator/auxiliary/norm_profiles/profiles_zuweisungen.csv"
    ),
) -> pd.DataFrame:
    """
    Reads the csv file profiles_zuweisungen
    Args:
        file_path: file to read

    Returns:
        dataframe
    """
    return pd.read_csv(file_path, sep=";", encoding="latin")


def read_occupancy_schedules_zuweisungen_data() -> pd.DataFrame:
    """
    Reads the csv file occupancy_schedules_zuweisungen
    Returns:
        dataframe
    """
    return pd.read_csv(
        os.path.join(
            "iso_simulator/auxiliary/occupancy_schedules/occupancy_schedules_zuweisungen.csv"
        ),
        sep=";",
        encoding="latin",
    )


def read_schedule_file(schedule_name) -> pd.DataFrame:
    """
    Reads the csv file schedule_name
    Args:
        schedule_name:

    Returns:
        dataframe
    """
    return pd.read_csv(
        os.path.join("iso_simulator/auxiliary/occupancy_schedules/")
        + schedule_name
        + ".csv",
        sep=";",
    )


def read_weather_data(epwfile_path: str) -> pd.DataFrame:
    """
    Reads the csv file epwfile_path
    Args:
        epwfile_path:

    Returns:
        dataframe
    """
    return pd.read_csv(epwfile_path, skiprows=8, header=None)


def read_vergleichswerte_zuweisung() -> pd.DataFrame:
    """
    Reads the csv file TEK_NWG_Vergleichswerte_zuweisung
    Returns:
        dataframe
    """
    return pd.read_csv(
        os.path.join(
            "iso_simulator/auxiliary/TEKs/TEK_NWG_Vergleichswerte_zuweisung.csv"
        ),
        sep=";",
        decimal=",",
        encoding="cp1250",
    )


def read_tek_nwg_vergleichswerte() -> pd.DataFrame:
    """
    Reads the csv file TEK_NWG_Vergleichswerte
    Returns:
        dataframe
    """
    return pd.read_csv(
        os.path.join("iso_simulator/auxiliary/TEKs/TEK_NWG_Vergleichswerte.csv"),
        sep=";",
        decimal=",",
        index_col=False,
        encoding="cp1250",
    )
