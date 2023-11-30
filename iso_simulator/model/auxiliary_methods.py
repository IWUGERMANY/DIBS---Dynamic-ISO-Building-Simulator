"""
Set the path to the project root directory and add it to the python path.
"""
from model.plz_data import PLZData
from typing import List

def get_coordinates_by_plz(plzData: List[PLZData], target_plz):

    """
    Returns the coordinates of the given PLZ.
    :param plzData: List of PLZData
    :param target_plz: Zipcode
    :return: Tuple of coordinates
    """

    for item in plzData:
        if item.zipcode == target_plz:
            return [item.latitude, item.longitude]
        