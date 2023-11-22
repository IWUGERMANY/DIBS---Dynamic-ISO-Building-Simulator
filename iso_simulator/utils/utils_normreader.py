import pandas as pd
import os
from typing import Tuple


def getValueError() -> ValueError:
    raise ValueError(
        'Something went wrong with the function getUsagetime()')


def getUsageStartEnd(usage_from_norm: str, row: pd.DataFrame) -> Tuple[int, int]:
    if usage_from_norm == 'sia2024':
        return int(row['usage_start_sia2024'].to_string(index=False).strip()), int(row['usage_end_sia2024'].to_string(index=False).strip())
    return int(row['usage_start_18599'].to_string(index=False).strip()), int(row['usage_end_18599'].to_string(index=False).strip())


def getApplianceGainsSIA2024(gains_from_group_values: str, row: pd.DataFrame) -> float:
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


def getApplianceGains18599(gains_from_group_values: str, row: pd.DataFrame) -> float:
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


def getTypNormAndGainPerPersonSIA2024(row: pd.DataFrame) -> Tuple[float, str]:
    return float(
        row['gain_per_person_sia2024'].to_string(index=False).strip()), row['typ_sia2024'].to_string(index=False).strip()


def getTypNormAndGainPerPerson18599(row: pd.DataFrame) -> Tuple[float, str]:
    return float(
        row['gain_per_person_18599'].to_string(index=False).strip()), row['typ_18599'].to_string(index=False).strip()


def getGainPerPersonAndApplianceAndTypNormSIA2024(gains_from_group_values: str, row: pd.DataFrame) -> Tuple[Tuple[float, str], float]:
    return getTypNormAndGainPerPersonSIA2024(row), [getApplianceGainsSIA2024(gains_from_group_values, row)]


def getGainPerPersonAndApplianceAndTypNorm18599(row, gains_from_group_values: str) -> Tuple[Tuple[float, str], float]:
    return getTypNormAndGainPerPerson18599(row), [getApplianceGains18599(gains_from_group_values, row)]

def findRow(gains_zuweisungen, uk_geb):
    return gains_zuweisungen[gains_zuweisungen['uk_geb'] == uk_geb]
