from schedule_name import ScheduleName
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

    def get(self):
        return self

    # def getScheduleObjects_and_schedule_name(self):
    #     if self.hk_geb is None and self.uk_geb is None:
    #         schedule_name = self.schedule_name.strip()

    #         csv_to_json = CSVToJSON(
    #             '../auxiliary/occupancy_schedules/'+schedule_name+'.csv')

    #         csv_to_json.convertCsvToJson()
    #         class_list = csv_to_json.createDynamicClassList(
    #             schedule_name)

    #         return class_list, schedule_name
