import sys
import os
import pandas as pd

mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mainPath)


def raise_exception(message: str):
    raise ValueError(f' {message} unbekannt')

def find_row(zuweisungen: pd.DataFrame, uk_geb: str) -> pd.DataFrame:
    return zuweisungen[zuweisungen['uk_geb'] == uk_geb]


def get_schedule_name(row: pd.DataFrame) -> str:
    return row['schedule_name'].to_string(index=False).strip()

