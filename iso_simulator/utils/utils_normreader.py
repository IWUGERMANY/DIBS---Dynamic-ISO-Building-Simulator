import pandas as pd

from typing import Tuple


def get_value_error() -> ValueError:
    raise ValueError(
        'Something went wrong with the function getUsagetime()')


def get_usage_start_end(usage_from_norm: str, row: pd.DataFrame) -> Tuple[int, int]:
    if usage_from_norm == 'sia2024':
        return int(row['usage_start_sia2024'].to_string(index=False).strip()), int(
            row['usage_end_sia2024'].to_string(index=False).strip())
    return int(row['usage_start_18599'].to_string(index=False).strip()), int(
        row['usage_end_18599'].to_string(index=False).strip())


def get_appliance_gains_sia2024(gains_from_group_values: str, row: pd.DataFrame) -> float:
    match gains_from_group_values:
        case 'low':
            appliance_gains = float(
                row['appliance_gains_ziel_sia2024'].to_string(index=False).strip())

        case 'mid':
            appliance_gains = float(
                row['appliance_gains_standard_sia2024'].to_string(index=False).strip())

        case 'max':
            appliance_gains = float(
                row['appliance_gains_bestand_sia2024'].to_string(index=False).strip())

    return appliance_gains


def get_appliance_gains_18599(gains_from_group_values: str, row: pd.DataFrame) -> float:
    match gains_from_group_values:
        case 'low':
            return float(
                row['appliance_gains_tief_18599'].to_string(index=False).strip())

        case 'mid':
            return float(
                row['appliance_gains_mittel_18599'].to_string(index=False).strip())

        case 'max':
            return float(
                row['appliance_gains_hoch_18599'].to_string(index=False).strip())


def get_typ_norm_and_gain_per_person_sia2024(row: pd.DataFrame) -> Tuple[float, str]:
    return float(
        row['gain_per_person_sia2024'].to_string(index=False).strip()), row['typ_sia2024'].to_string(
        index=False).strip()


def get_typ_norm_and_gain_per_person_18599(row: pd.DataFrame) -> Tuple[float, str]:
    return float(
        row['gain_per_person_18599'].to_string(index=False).strip()), row['typ_18599'].to_string(index=False).strip()


def get_gain_per_person_and_appliance_and_typ_norm_sia2024(gains_from_group_values: str, row: pd.DataFrame) -> Tuple[
    Tuple[float, str], float]:
    return get_typ_norm_and_gain_per_person_sia2024(row), get_appliance_gains_sia2024(gains_from_group_values, row)


def get_gain_per_person_and_appliance_and_typ_norm_18599(row, gains_from_group_values: str) -> Tuple[
    Tuple[float, str], float]:
    return get_typ_norm_and_gain_per_person_18599(row), get_appliance_gains_18599(gains_from_group_values, row)


def find_row(gains_zuweisungen: pd.DataFrame, uk_geb: str) -> pd.DataFrame:
    return gains_zuweisungen[gains_zuweisungen['uk_geb'] == uk_geb]
