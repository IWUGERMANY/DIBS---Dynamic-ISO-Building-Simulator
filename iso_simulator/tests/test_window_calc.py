import unittest
from iso_simulator.building_simulator.building_simulator import BuildingSimulator
from iso_simulator.data_source.datasource_csv import DataSourceCSV


class TestBuildingCalculations(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.building_simulator = BuildingSimulator(
            DataSourceCSV(), "2004-2018", 'din18599', 'mid')
        self.weather_data = self.building_simulator.get_weather_data()

    def test_calc_solar_gains_and_incident_south_window_hour0(self):
        self.building_simulator.calc_solar_gains_for_all_windows(
            self.weather_data, -60.95945850498123, 160.65950615649393, 21, 0)
        south_window = self.building_simulator.all_windows[0]
        self.assertTrue(south_window.solar_gains ==
                         0.0 and south_window.incident_solar == 0.0)

    def test_calc_solar_gains_and_incident_south_window_hour1(self):
        self.building_simulator.calc_solar_gains_for_all_windows(
            self.weather_data, -55.95931958767895, 135.85871354377173, 20.999999999999993, 1)
        south_window = self.building_simulator.all_windows[0]
        self.assertTrue(south_window.solar_gains ==
                         0.0 and south_window.incident_solar == 0.0)

    def test_calc_solar_gains_and_incident_south_window_hour8(self):
        self.building_simulator.calc_solar_gains_for_all_windows(
            self.weather_data, 3.9679769725374214, 44.92407457491144, 21.0, 8)
        south_window = self.building_simulator.all_windows[0]
        self.assertTrue(south_window.solar_gains ==
                         17.85620126745 and south_window.incident_solar == 22.8925657275)

    def test_calc_solar_gains_and_incident_south_window_hour457(self):
        self.building_simulator.calc_solar_gains_for_all_windows(
            self.weather_data, -54.34223824761903, 140.6194854215748, 20.999999999999996, 457)
        south_window = self.building_simulator.all_windows[0]
        self.assertTrue(south_window.solar_gains ==
                         0.0 and south_window.incident_solar == 0.0)
        
    def test_calc_solar_gains_and_incident_south_window_hour1269(self):
        self.building_simulator.calc_solar_gains_for_all_windows(
            self.weather_data, -39.5393918672982, 230.92486360450772, 20.999999999999996, 1269)
        south_window = self.building_simulator.all_windows[0]
        self.assertTrue(south_window.solar_gains ==
                         0.0 and south_window.incident_solar == 0.0)
