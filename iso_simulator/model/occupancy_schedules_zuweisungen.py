from .schedule_name import ScheduleName
from typing import List


class OccupancySchedulesAssignment:

    def __init__(self,
                 hk_geb: str,
                 uk_geb: str,
                 schedule_name: str
                 ):

        self.hk_geb = hk_geb
        self.uk_geb = uk_geb
        self.schedule_name = schedule_name