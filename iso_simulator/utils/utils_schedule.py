import sys
import os
import pandas as pd

mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mainPath)


def raiseException(message):
    raise ValueError(f' {message} unbekannt')

def findRow(zuweisungen, uk_geb):
    return zuweisungen[zuweisungen['uk_geb'] == uk_geb]


def getScheduleName(row):
    return row['schedule_name'].to_string(index=False).strip()

