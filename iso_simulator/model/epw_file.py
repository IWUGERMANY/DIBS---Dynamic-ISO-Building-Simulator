from typing import Tuple

class EPWFile:

    def __init__(self,
                 file_name: str,
                 coordinates_station: Tuple[float, float],
                 distance: float
                 ):
        
        self.file_name = file_name
        self.coordinates_station = coordinates_station
        self.distance = distance
        