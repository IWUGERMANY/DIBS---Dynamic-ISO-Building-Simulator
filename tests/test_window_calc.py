import unittest
from iso_simulator.building_simulator.simulator import BuildingSimulator
from iso_simulator.data_source.datasource_csv import DataSourceCSV


class TestBuildingCalculations(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.building_simulator = BuildingSimulator(
            DataSourceCSV(), "2004-2018", 'din18599', 'mid', 'sia2024')
        self.weather_data = self.building_simulator.get_weather_data()

    def test_calc_solar_gains_and_incident_south_window_hour0(self):
        self.building_simulator.calc_solar_gains_for_all_windows(-60.95945850498123, 160.65950615649393, 21, 0)
        south_window = self.building_simulator.all_windows[0]
        self.assertTrue(south_window.solar_gains ==
                        0.0 and south_window.incident_solar == 0.0)

    def test_calc_solar_gains_and_incident_south_window_hour1(self):
        self.building_simulator.calc_solar_gains_for_all_windows(-55.95931958767895, 135.85871354377173,
                                                                 20.999999999999993, 1)
        south_window = self.building_simulator.all_windows[0]
        self.assertTrue(south_window.solar_gains ==
                        0.0 and south_window.incident_solar == 0.0)

    def test_calc_solar_gains_and_incident_south_window_hour8(self):
        self.building_simulator.calc_solar_gains_for_all_windows(3.9679769725374214, 44.92407457491144, 21.0, 8)
        south_window = self.building_simulator.all_windows[0]
        self.assertTrue(south_window.solar_gains ==
                        17.85620126745 and south_window.incident_solar == 22.8925657275)

    def test_calc_solar_gains_and_incident_south_window_hour457(self):
        self.building_simulator.calc_solar_gains_for_all_windows(-54.34223824761903, 140.6194854215748,
                                                                 20.999999999999996, 457)
        south_window = self.building_simulator.all_windows[0]
        self.assertTrue(south_window.solar_gains ==
                        0.0 and south_window.incident_solar == 0.0)

    def test_calc_solar_gains_and_incident_south_window_hour1269(self):
        self.building_simulator.calc_solar_gains_for_all_windows(-39.5393918672982, 230.92486360450772,
                                                                 20.999999999999996, 1269)
        south_window = self.building_simulator.all_windows[0]
        self.assertTrue(south_window.solar_gains ==
                        0.0 and south_window.incident_solar == 0.0)

    def test_calc_solar_gains_and_incident_north_window_hour493(self):
        self.building_simulator.calc_solar_gains_for_all_windows(16.018340805027727, -22.59108487786433,
                                                                 21.000000000000018, 493)
        north_window = self.building_simulator.all_windows[3]
        self.assertTrue(north_window.solar_gains ==
                        1280.5665176678137 and north_window.incident_solar == 1641.7519457279664)

    def test_calc_solar_gains_and_incident_north_window_hour565(self):
        self.building_simulator.calc_solar_gains_for_all_windows(16.69291977700871, -22.571355385149154,
                                                                 20.999999999999993, 565)
        north_window = self.building_simulator.all_windows[3]
        self.assertTrue(north_window.solar_gains ==
                        1325.3766159109364 and north_window.incident_solar == 1699.2007896294056)

    def test_calc_solar_gains_and_incident_east_window_hour61(self):
        self.building_simulator.calc_illuminance_for_all_windows(12.997110123176972, -23.407778306337853, 61)
        east_window = self.building_simulator.all_windows[1]
        self.assertTrue(east_window.incident_illuminance ==
                        104718.2186794875 and east_window.transmitted_illuminance == 35141.339824462404)

    def test_calc_solar_gains_and_incident_east_window_hour83(self):
        self.building_simulator.calc_illuminance_for_all_windows(16.122647926740026, 5.060703532221619, 83)
        east_window = self.building_simulator.all_windows[1]
        self.assertTrue(east_window.incident_illuminance ==
                        137889.5615793399 and east_window.transmitted_illuminance == 46272.97907479487)

    def test_illuminance_sum_hour0(self):
        self.building_simulator.calc_illuminance_for_all_windows(-60.95945850498123, 160.65950615649393, 0)
        self.assertEqual(self.building_simulator.calc_sum_illuminance_all_windows(), 0.0)

    def test_illuminance_sum_hour83(self):
        self.building_simulator.calc_illuminance_for_all_windows(16.122647926740026, 5.060703532221619, 83)
        self.assertEqual(self.building_simulator.calc_sum_illuminance_all_windows(), 186325.35260278248)

    def test_sum_solar_gains_hour0(self):
        self.building_simulator.calc_solar_gains_for_all_windows(-60.95945850498123, 160.65950615649393, 21, 0)
        self.assertEqual(self.building_simulator.calc_sum_solar_gains_all_windows(), 0.0)

    def test_sum_solar_gains_hour517(self):
        self.building_simulator.calc_solar_gains_for_all_windows(16.23818242835413, -22.580438049800044,
                                                                 20.999999999999982, 517)
        self.assertEqual(self.building_simulator.calc_sum_solar_gains_all_windows(), 13424.628016566767)

    def test_sum_solar_gains_hour534(self):
        self.building_simulator.calc_solar_gains_for_all_windows(-10.333686435884786, 71.36244746839664,
                                                                 20.999999999999993, 534)
        self.assertEqual(self.building_simulator.calc_sum_solar_gains_all_windows(), 0.0)

    def test_sum_solar_gains_hour1983(self):
        self.building_simulator.calc_solar_gains_for_all_windows(22.26209150086465, -61.24767153345493,
                                                                 21.000000000000004, 1983)
        self.assertEqual(self.building_simulator.calc_sum_solar_gains_all_windows(), 7472.380143437347)
