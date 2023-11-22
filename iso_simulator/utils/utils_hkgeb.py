import sys
import os
mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mainPath)


def hkInZuweisungen(hk_geb, gains_zuweisungen):
    return hk_geb in gains_zuweisungen['hk_geb'].values

def ukInZuweisungen(uk_geb, gains_zuweisungen):
    return uk_geb in gains_zuweisungen['uk_geb'].values

def hkAndUkInZuweisungen(gains_zuweisungen, hk_geb, uk_geb):
    return hkInZuweisungen(hk_geb, gains_zuweisungen) and ukInZuweisungen(uk_geb, gains_zuweisungen)