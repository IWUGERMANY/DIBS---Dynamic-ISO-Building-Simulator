"""
This file contains auxiliary functions which used to check if the hk_geb (Usage type (main category)) or uk_geb
(Usage type (subcategory)) are contained in the imported csv files
"""

import sys
import os

from pandas import DataFrame

mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mainPath)


def hk_in_zuweisungen(hk_geb: str, gains_zuweisungen: DataFrame) -> bool:
    return hk_geb in gains_zuweisungen['hk_geb'].values


def uk_in_zuweisungen(uk_geb: str, gains_zuweisungen: DataFrame) -> bool:
    return uk_geb in gains_zuweisungen['uk_geb'].values


def hk_and_uk_in_zuweisungen(gains_zuweisungen: DataFrame, hk_geb: str, uk_geb: str) -> bool:
    return hk_in_zuweisungen(hk_geb, gains_zuweisungen) and uk_in_zuweisungen(uk_geb, gains_zuweisungen)


def hk_or_uk_not_in_zuweisungen(zuweisungen, hk_geb, uk_geb):
    return not hk_in_zuweisungen(hk_geb, zuweisungen) or not uk_in_zuweisungen(uk_geb, zuweisungen)
