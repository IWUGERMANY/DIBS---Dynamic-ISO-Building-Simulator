from typing import List


class ScheduleName:

    def __init__(self,
                 People: float,
                 Appliances: float
                 ):
        self.People = People,
        self.Appliances = Appliances


class ScheduleNameList:

    def __init__(self):
        pass

    # def __init__(self, csv_to_json: CSVToJSON):
    #     self.csv_to_json = csv_to_json
    #     self.schedule_name_list: List[ScheduleName] = self.csv_to_json.createDynamicClassList(
    #         "ScheduleName")

    # def add_schedule_name(self, schedule_name: ScheduleName):
    #     self.schedule_name_list.append(schedule_name)

    # def get_schedule_name_list(self) -> List[ScheduleName]:
    #     return self.schedule_name_list
