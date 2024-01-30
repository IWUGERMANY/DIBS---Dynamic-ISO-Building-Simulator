from typing import List

__author__ = "Wail Samjouni"
__copyright__ = "Copyright 2023, Institut Wohnen und Umwelt"
__license__ = "MIT"


class EPWFile:

    """
    Sets the parameters of the EPWFile.

    Args:
        file_name: The name of the EPW file
        coordinates_station: The coordinates of the station
        distance: The nearest distance between the station and the building
    """

    def __init__(self, file_name: str, coordinates_station: List, distance: float):
        self.file_name = file_name
        self.coordinates_station = coordinates_station
        self.distance = distance
