import sys
import os
import pandas as pd

mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mainPath)

def readVergleichswerteZuweisung():
    return pd.read_csv(os.path.join('../auxiliary/TEKs/TEK_NWG_Vergleichswerte_zuweisung.csv'), sep = ';', decimal=',', encoding = 'cp1250')

def readTEKNWGVergleichswerte():
    return pd.read_csv(os.path.join('../auxiliary/TEKs/TEK_NWG_Vergleichswerte.csv'), sep = ';', decimal=',', index_col = False, encoding = 'cp1250')

def getTekName(row):
    TEK_name = row['TEK'].astype(str)
    return TEK_name.iloc[0]

def getTEKDataFrameBasedOnTEKName(DB_TEKs, TEK_name):
    return DB_TEKs[DB_TEKs['TEK_Category'] == TEK_name]

def getTEKDhw(df_TEK):
    TEK_dhw = df_TEK.iloc[0]['TEK Warmwasser']
    return TEK_dhw.astype(float)

def hkInZuweisungen(hk_geb, zuweisungen):
    return hk_geb in zuweisungen['hk_geb'].values

def ukInZuweisungen(uk_geb, zuweisungen):
    return uk_geb in zuweisungen['uk_geb'].values

def hkOrUkNotInZuweisungen(zuweisungen, hk_geb, uk_geb):
    return not hkInZuweisungen(hk_geb, zuweisungen) or not ukInZuweisungen(uk_geb, zuweisungen)