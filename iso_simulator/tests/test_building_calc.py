from iso_simulator.data_source.datasource_csv import DataSourceCSV
from iso_simulator.building_simulator import BuildingSimulator
import unittest


class TestBuildingCalculations(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.building = DataSourceCSV().get_building_data()

    def test_mass_area(self):
        self.assertEqual(self.building.mass_area, 529.0120000000001,
                         'Mass area should be 529.0120000000001')

    def test_window_area(self):
        self.assertEqual(self.building.window_area, 92.5809926975,
                         'Window area should be 92.5809926975')

    def building_volume(self):
        self.assertEqual(self.building.building_vol(
        ), 681.3674418930134, 'Building volume should be 681.3674418930134')

    def test_total_internal_area(self):
        self.assertEqual(self.building.total_internal_area, 952.2216000000001,
                         'Total internal area should be 952.2216000000001')

    def test_a_t(self):
        self.assertEqual(self.building.A_t, 952.2216000000001,
                         'A_t should be 952.2216000000001')

    def test_c_m(self):
        self.assertEqual(self.building.c_m, 211.6048, 'c_m should be 211.6048')

    def test_h_tr_op(self):
        self.assertEqual(self.building.h_tr_op, 759.6174183333334,
                         'h_tr_op should be 759.6174183333334')

    def test_h_tr_w(self):
        self.assertEqual(self.building.h_tr_w, 157.38768758574997,
                         'h_tr_w should be 157.38768758574997')

    def test_ach_tot(self):
        self.assertEqual(self.building.ach_tot, 1.3422360505638933,
                         'ach_tot should be 1.3422360505638933')

    def test_b_ek(self):
        self.assertEqual(self.building.b_ek, 1.0, 'b_ek should be 1.0')

    def test_h_tr_ms(self):
        self.assertEqual(self.building.h_tr_ms, 4814.0092,
                         'h_tr_ms should be 4814.0092')

    def test_h_tr_is(self):
        self.assertEqual(self.building.h_tr_is, 3285.1645200000003,
                         'h_tr_is should be 3285.1645200000003')

    def test_h_tr_em(self):
        self.assertEqual(self.building.h_tr_em, 901.9368224038989,
                         'h_tr_em should be 901.9368224038989')

    def test_b(self):
        self.assertFalse(
            self.building.has_heating_demand and self.building.has_cooling_demand)

    def test_t_out(self):
        building_simulator = BuildingSimulator(
            DataSourceCSV(), "2004-2018", 'din', 'low')
        weather_data = building_simulator.get_weather_data()
        self.assertEqual(building_simulator.extract_outdoor_temperature(
            weather_data, 2), -2.00)

    def test_h_ve_adj(self):
        self.assertEqual(self.building.calc_h_ve_adj(
            1, -7.0, 7, 18), 74.59130885432073, 'Result should be 74.5913088543207')

    def test_h_ve_adj_hour31(self):
        self.assertEqual(self.building.calc_h_ve_adj(
            31, -1.0, 7, 18), 230.260672542113, 'Result should be 230.260672542113')

    def test_h_ve_adj_hour186(self):
        self.assertEqual(self.building.calc_h_ve_adj(
            186, 10.0, 7, 18), 74.59130885432073, 'Result should be 74.5913088543207')

    def test_check_night_flushing(self):
        self.building.calc_h_ve_adj(186, 10.0, 7, 18)
        self.assertFalse(self.building.night_flushing_on)

    def test_altitude_and_azimuth_hour0(self):
        building_simulator = BuildingSimulator(
            DataSourceCSV(), "2004-2018", 'din18599', 'mid')
        self.assertEqual(building_simulator.get_altitude_and_zimuth(
            0), (-60.95945850498123, 160.65950615649393))

    def test_altitude_and_azimuth_hour6(self):
        building_simulator = BuildingSimulator(
            DataSourceCSV(), "2004-2018", 'din18599', 'mid')
        self.assertEqual(building_simulator.get_altitude_and_zimuth(
            6), (-11.68415334313391, 67.73680832995645))
        
    def test_altitude_and_azimuth_hour12(self):
        building_simulator = BuildingSimulator(
            DataSourceCSV(), "2004-2018", 'din18599', 'mid')
        self.assertEqual(building_simulator.get_altitude_and_zimuth(
            12), (15.475326045849297, -9.602544290526064))