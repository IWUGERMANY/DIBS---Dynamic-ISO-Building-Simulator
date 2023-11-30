import unittest
from iso_simulator.building_simulator.building_simulator import BuildingSimulator

from iso_simulator.data_source.datasource_csv import DataSourceCSV


class TestScheduleCalculations(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.building_simulator = BuildingSimulator(
            DataSourceCSV(), "2004-2018", 'din18599', 'mid')
        self.building = self.building_simulator.datasourcecsv.get_building_data()

    def test_get_schedule(self):
        occupancy_schedule, schedule_name = self.building_simulator.get_schedule()
        self.assertTrue(len(occupancy_schedule) ==
                        8760 and schedule_name == 'Bueros_SchalterhalleEmpfang')

    def test_occupancy_full_usage_hours(self):
        self.assertEqual(self.building_simulator.get_occupancy_full_usage_hours(), 1503.3600000000001)
    

