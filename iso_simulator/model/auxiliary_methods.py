import os, sys

mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mainPath)

from model.plz_data import PLZData
from typing import List

def getCoordinatesByPLZ(plzData: List[PLZData], target_plz):

    for item in plzData:
        if item.zipcode == target_plz:
            return [item.latitude, item.longitude]
        