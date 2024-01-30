import pandas as pd


def find_row(zuweisungen: pd.DataFrame, uk_geb: str) -> pd.DataFrame:
    return zuweisungen[zuweisungen["uk_geb"] == uk_geb]


def get_schedule_name(row: pd.DataFrame) -> str:
    return row["schedule_name"].to_string(index=False).strip()
