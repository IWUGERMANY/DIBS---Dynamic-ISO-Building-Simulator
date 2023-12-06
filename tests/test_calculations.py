import unittest
from iso_simulator.building_simulator.simulator import BuildingSimulator
from iso_simulator.data_source.datasource_csv import DataSourceCSV


class TestCalculations(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.building_simulator = BuildingSimulator(
            DataSourceCSV(), "2004-2018", 'din18599', 'mid')
        self.building = self.building_simulator.datasourcecsv.get_building_data()

    def test_tek_dhw_and_name(self):
        tek_dhw, tek_name = self.building_simulator.get_tek()
        self.assertTrue(tek_dhw == 7.1 and tek_name == 'Feuerwehrdienstgebäude')

    def test_calc_occupancy_hour0(self):
        schedules, schedule_name = self.building_simulator.get_schedule()
        occupancy = self.building_simulator.calc_occupancy(schedules, 0)
        self.assertEqual(occupancy, 0.0)

    def test_calc_occupancy_hour11(self):
        schedules, schedule_name = self.building_simulator.get_schedule()
        occupancy = self.building_simulator.calc_occupancy(schedules, 11)
        self.assertEqual(occupancy, 8.320000000000002)

    def test_calc_occupancy_hour130(self):
        schedules, schedule_name = self.building_simulator.get_schedule()
        occupancy = self.building_simulator.calc_occupancy(schedules, 130)
        self.assertEqual(occupancy, 10.4)

    def test_calc_internal_gains_hour0(self):
        self.building_simulator.building_object.solve_building_lighting(0.0, 0.0)
        schedules, schedule_name = self.building_simulator.get_schedule()
        self.assertEqual(
            self.building_simulator.calc_gains_from_occupancy_and_appliances(schedules, 0.0, 70.0, 10.0, 0),
            169.28384000000003)

    def test_calc_internal_gains_hour83(self):
        self.building_simulator.building_object.solve_building_lighting(186325.35260278248, 0.0)
        schedules, schedule_name = self.building_simulator.get_schedule()
        self.assertEqual(
            self.building_simulator.calc_gains_from_occupancy_and_appliances(schedules, 0.0, 70.0, 10.0, 83),
            169.28384000000003)

    def test_calc_appliance_gains_demand_hour83(self):
        schedules, schedule_name = self.building_simulator.get_schedule()
        self.assertEqual(self.building_simulator.calc_appliance_gains_demand(schedules, 10.0, 83), 169.28384000000003)

    def test_get_appliance_gains_elt_demand_hour83(self):
        schedules, schedule_name = self.building_simulator.get_schedule()
        self.assertEqual(self.building_simulator.get_appliance_gains_elt_demand(schedules, 10.0, 83),
                         169.28384000000003)

    def test_get_appliance_gains_elt_demand_hour135(self):
        schedules, schedule_name = self.building_simulator.get_schedule()
        self.assertEqual(self.building_simulator.get_appliance_gains_elt_demand(schedules, 10.0, 153),
                         1354.2707200000004)

    def test_energy_and_sys_electricity_calculations_hour0(self):
        self.building_simulator.building_object.solve_building_energy(169.28384000000003, 0.0, -7.0, 21)
        tek_dhw, tek_name = self.building_simulator.get_tek()
        full_usage = self.building_simulator.get_occupancy_full_usage_hours()
        schedules, schedule_name = self.building_simulator.get_schedule()
        result = self.building_simulator.calc_hot_water_usage(schedules, tek_dhw / full_usage, 0)
        self.assertTrue(
            result.hotwaterenergy == 0.0 and result.HotWaterSysElectricity == 0.0 and result.hotwaterdemand == 0.0 and result.HotWater_Sys_Fossils == 0.0)
