import pandas as pd


def get_tek_name(row: pd.DataFrame) -> str:
    return row['TEK'].astype(str).iloc[0]

def get_tek_data_frame_based_on_tek_name(DB_TEKs: pd.DataFrame, TEK_name: str) -> pd.DataFrame:
    return DB_TEKs[DB_TEKs['TEK_Category'] == TEK_name]

def get_tek_dhw(df_TEK: pd.DataFrame) -> float:
    TEK_dhw = df_TEK.iloc[0]['TEK Warmwasser']
    return TEK_dhw.astype(float)