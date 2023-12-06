from typing import List, Union

from iso_simulator.model.plz_data import PLZData

def get_coordinates_by_plz(plzData: List[PLZData], target_plz: str) -> Union[List, ValueError]:

    """
    Returns the coordinates of the given PLZ.
    :param plzData: List of PLZData
    :param target_plz: Zipcode
    :return: Tuple of coordinates
    """

    for item in plzData:
        if item.zipcode == target_plz:
            return [item.latitude, item.longitude]
    return ValueError('Postleitzahl nicht gefunden')
        